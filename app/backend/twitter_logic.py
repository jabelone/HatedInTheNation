# The core twitter logic for CAB432 Assessment (individual project)
# Student Name: Jaimyn Mayer (n9749331)

import my_models
import requests
import json
import os
import twitter
import datetime


class twitter_scraper():
    api = None  # our twitter API instance
    # the tags to follow, only here for reference, you MUST specify at least one
    follow_tags = [
        {
            "tag": "@NO_TAGS_SPECIFIED",
            "profile": "/static/images/billshorten.jpg",
            "displayname": "No Tags Specified"
        }
    ]
    microsoft_headers = {}  # the authentication header for the Microsoft API
    debug_level = False  # print some stuff if set to True

    # urls of all the endpoints we need to use
    find_places_api = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    microsoft_api = "https://australiaeast.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment"
    ibm_api = "https://gateway-syd.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21"

    def __init__(self, follow_tags, debug_level=0):
        if debug_level:
            self.debug_level = debug_level
            self.debug("set debug level to: " + str(debug_level), 3)

        if len(follow_tags):
            self.follow_tags = follow_tags

        else:
            raise RuntimeError("No tags specified. You must specify tags to follow.")

        # all of these environment variables are needed to run
        needed_vars = (
            "TWITTER_CONSUMER_KEY",
            "TWITTER_CONSUMER_SECRET",
            "TWITTER_ACCESS_TOKEN_KEY",
            "TWITTER_ACCESS_TOKEN_SECRET",
            "GOOGLE_FIND_PLACES",
            "MICROSOFT_API",
        )

        # check if all of the environment variables exist
        for var in needed_vars:
            if var not in os.environ:
                self.debug("missing environment variable: " + var, 1)
                raise RuntimeError("Missing environment variable: " + var)

        self.microsoft_headers = {"Ocp-Apim-Subscription-Key": os.environ.get("MICROSOFT_API")}

        # init our twitter API instance
        self.api = twitter.Api(consumer_key=os.environ.get("TWITTER_CONSUMER_KEY"),
                               consumer_secret=os.environ.get("TWITTER_CONSUMER_SECRET"),
                               access_token_key=os.environ.get("TWITTER_ACCESS_TOKEN_KEY"),
                               access_token_secret=os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
                               tweet_mode="extended")

        # this ensures we only cache results for 3 seconds, meaning it shouldn't be possible to hit a rate limit.
        # this also means we get fresh data every time we hit their API.
        self.debug("setting twitter cache to 3 seconds", 3)
        self.api.SetCacheTimeout(3)

    def debug(self, string, value=1):
        if value <= self.debug_level:
            print(string.encode('utf-8'))

    def process_user(self, tweet):
        print(tweet)
        user = my_models.User.get_or_create(
            username=tweet.user.screen_name)  # try getting the user or create one if they don't exist
        new = user[1]  # this boolean is True if the entry was created in the db
        user = user[0]  # this is the user object

        # if the username isn't in the database
        if new:
            self.debug("~~ created new user: " + user.username, 1)

            if len(tweet.user.location) < 3:
                self.debug("user location too short, not localising: " + tweet.user.location, 3)
                return False

            payload = {
                "input": tweet.user.location,
                "inputtype": "textquery",
                "fields": "formatted_address,name",
                "locationbias": "ipbias",
                "language": "en-Au",
                "key": os.environ.get("GOOGLE_FIND_PLACES")
            }

            # normalise the users location so we can pull the state out of it
            self.debug("attempting to normalise location", 3)
            normalised_location = requests.get(self.find_places_api, params=payload).json()

            # if the Google API was successful then save their location and attempt to recognise the state
            if normalised_location["status"] == "OK":
                user.raw_location = tweet.user.location

                # try to extract the normalised location and return false if it can't find one
                # this is needed because sometimes the API returns an empty list, even if it says it's status is OK :/
                try:
                    user.normalised_location = str(normalised_location["candidates"][0]["formatted_address"]).lower()
                except KeyError:
                    self.debug("normalisation failed, removing user", 3)
                    return False

                # couldn't think of a better way as the address is returned as a string with 2 formats
                if " nsw" in user.normalised_location or "new south wales" in user.normalised_location:
                    user.state = "NSW"
                elif " vic" in user.normalised_location or "victoria" in user.normalised_location:
                    user.state = "VIC"
                elif " qld" in user.normalised_location or "queensland" in user.normalised_location:
                    user.state = "QLD"
                elif " act" in user.normalised_location or "australian capital territory" in user.normalised_location:
                    user.state = "ACT"
                elif " wa" in user.normalised_location or "western australia" in user.normalised_location:
                    user.state = "WA"
                elif " nt" in user.normalised_location or "northern territory" in user.normalised_location:
                    user.state = "NT"
                elif " tas" in user.normalised_location or "tasmania" in user.normalised_location:
                    user.state = "TAS"
                elif " sa" in user.normalised_location or "south australia" in user.normalised_location:
                    user.state = "TAS"
                elif "australia" in user.normalised_location:
                    # this special case is when the users location is just Australiawith
                    # we're still interested in it because it's extra data for the australia wide sentiment analysis
                    user.state = "UNKNOWN"
                else:
                    user.state = "INTERNATIONAL"

                self.debug("found new user from {}".format(user.state), 1)

                # save and return our user instance
                user.save()
                return user

            else:
                # if we couldn't normalise a location, return false and trash the user
                self.debug("normalisation failed", 3)
                return False
        else:
            self.debug("~~ user already exists: " + user.username, 3)
            return user

    def add_tweet(self, result):
        """
        This method will attempt to add a tweet to our db.
        :param result:
        :return:
        """

        # process the username (add to db if not there, otherwise get instance)
        self.debug("attempting to process user: " + result.user.screen_name, 2)
        user = self.process_user(result)

        if not user:
            return False

        # create a new tweet, or return the model instance if it exists
        tweet = my_models.Tweet.get_or_create(snowflake=result.id, user_id=user.username)

        # if a new tweet was created add the data, save it then return it
        if tweet[1]:
            tweet = tweet[0]
            tweet.user = user
            tweet.text = result.full_text
            tweet.likes = result.favorite_count
            tweet.retweets = result.retweet_count
            tweet.save()

            self.debug("saved tweet to db", 1)
            return True

        # if the tweet already exists, just exit
        else:
            self.debug("tweet already exists in db", 2)
            return False

    def analyse_tweet_sentiment(self, tweet):
        """
        This method will run Microsoft sentiment analysis on the tweet and return the result.
        :param tweet:
        :return float:
        """
        payload = {
            "documents": [
                {
                    "language": "en",
                    "id": "1",
                    "text": tweet.full_text
                }]
        }

        tweet = my_models.Tweet.get_by_id(tweet.id)

        # Run our sentiment analysis on the tweet
        self.debug("attempting to run sentiment analysis on: " + tweet.text.strip(), 3)
        sentiment = requests.post(self.microsoft_api, data=json.dumps(payload), headers=self.microsoft_headers).json()
        tweet.sentiment = sentiment["documents"][0]["score"]
        tweet.save()
        self.debug("sentiment analysis complete: " + str(tweet.sentiment), 2)
        return True

    def scrape_twitter(self):
        self.debug(datetime.datetime.now().strftime('%H:%M:%S') + " - scraping twitter", 1)
        search_term = ""

        for x, tag in enumerate(self.follow_tags):
            if x == 0:
                search_term += tag["tag"]
            else:
                search_term += " OR " + tag["tag"]

        search_term += " -filter:retweets"
        results = self.api.GetSearch(term=search_term, lang="en", result_type="mixed", include_entities=True, count=10)

        # this one has a geocode restriction, it returns way less tweets but is guaranteed to be in Australia
        # results = api.GetSearch(term="@billshortenmp OR @ScottMorrisonMP OR @PaulineHansonOz -filter:retweets",
        #                    max_id=models.Tweet.select().limit(1)[0].snowflake, geocode="-27.532239,134.597291,2200km",
        #                    lang="en", result_type="mixed", include_entities=True, count=10)

        # results = self.api.GetSearch(term="#australia -filter:retweets",
        #                              lang="en", result_type="mixed",
        #                              include_entities=True, count=3)

        for result in results:
            # attempt to add the tweet, if successful, then run sentiment analysis on it
            if self.add_tweet(result):
                if self.analyse_tweet_sentiment(result):
                    self.debug("created user, added tweet and analysed it: " + str(result.full_text).rstrip(), 1)
