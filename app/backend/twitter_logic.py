# The core twitter logic for CAB432 Assessment (individual project)
# Student Name: Jaimyn Mayer (n9749331)

import my_models
import requests
import json
import os
import twitter
import datetime


class TwitterScraper:
    """
    Our twitter scraper class. Initialise with a list of tags to follow and an optional debug level.
    """
    api = None  # our twitter API instance
    # the tags to follow, only here for reference, you MUST specify at least one when initialising
    follow_tags = [
        {
            "tag": "@NO_TAGS_SPECIFIED",
            "profile": "/static/images/billshorten.jpg",
            "displayname": "No Tags Specified"
        }
    ]
    microsoft_headers = {}  # the authentication header for the Microsoft API
    debug_level = False  # print some stuff if set to True

    # URLs of all the endpoints we need to use.
    find_places_api = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    microsoft_api = "https://australiaeast.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment"
    ibm_api = "https://gateway-syd.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21"

    def __init__(self, follow_tags, debug_level=0):
        """
        Our twitter scraper class initialisation method. Must specify at least follow_tags.
        :param follow_tags:
        :param debug_level:
        """

        # If the debug level has been specified, save it to the instance.
        if debug_level:
            self.debug_level = debug_level
            self.debug("set debug level to: " + str(debug_level), 3)

        # If a list of tags to follow is specified, save it to the instance.
        if len(follow_tags):
            self.follow_tags = follow_tags

        else:
            raise RuntimeError("No tags specified. You must specify tags to follow.")

        # All of these environment variables are needed to run.
        needed_vars = (
            "TWITTER_CONSUMER_KEY",
            "TWITTER_CONSUMER_SECRET",
            "TWITTER_ACCESS_TOKEN_KEY",
            "TWITTER_ACCESS_TOKEN_SECRET",
            "GOOGLE_FIND_PLACES",
            "MICROSOFT_API",
        )

        # Check if all of the environment variables exist and raise an exception if any of them don't.
        for var in needed_vars:
            if var not in os.environ:
                self.debug("missing environment variable: " + var, 1)
                raise RuntimeError("Missing environment variable: " + var)

        self.microsoft_headers = {"Ocp-Apim-Subscription-Key": os.environ.get("MICROSOFT_API")}

        # Initialise our twitter API instance.
        self.api = twitter.Api(consumer_key=os.environ.get("TWITTER_CONSUMER_KEY"),
                               consumer_secret=os.environ.get("TWITTER_CONSUMER_SECRET"),
                               access_token_key=os.environ.get("TWITTER_ACCESS_TOKEN_KEY"),
                               access_token_secret=os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
                               tweet_mode="extended")

        # This ensures we only cache results for 3 seconds, meaning it shouldn't be possible to hit their rate limit.
        # This also means we get fresh data almost every time we hit their API.
        self.debug("setting twitter cache to 3 seconds", 3)
        self.api.SetCacheTimeout(3)

    def debug(self, string, value=1):
        """
        Convenience debug function. Prints the specified debug string if the instance's level is greater than specified.
        :param string:
        :param value:
        :return:
        """
        if value <= self.debug_level:
            print(string.encode('utf-8'))

    def process_user(self, tweet):
        """
        Our process user method attempts to add the user to the db and normalise their location.
        :param tweet:
        :return:
        """
        user = my_models.User.get_or_create(
            username=tweet.user.screen_name)  # Try getting the user or create one if they don't exist.
        new = user[1]  # This boolean is True if the entry was created in the db.
        user = user[0]  # This is the user object, whether we create a new one or it's existing.

        # If the user isn't in the database.
        if new:
            self.debug("~~ created new user: " + user.username, 1)

            if len(tweet.user.location) < 3:
                self.debug("user location too short, not localising: " + tweet.user.location, 3)
                return False

            # This is the payload for the first stage of location normalisation.
            payload = {
                "input": tweet.user.location,
                "inputtype": "textquery",
                "fields": "formatted_address,name",
                "locationbias": "ipbias",
                "language": "en-Au",
                "key": os.environ.get("GOOGLE_FIND_PLACES")
            }

            # Normalise the users location so we can pull the state out of it.
            self.debug("attempting to normalise location", 3)
            normalised_location = requests.get(self.find_places_api, params=payload).json()

            # If the Google API was successful then save their location and attempt to recognise the state.
            if normalised_location["status"] == "OK":
                user.raw_location = tweet.user.location

                # Try to extract the normalised location and return false if it can't find one.
                # This is needed because sometimes the API returns an empty list, even if it says it was OK. :/
                try:
                    user.normalised_location = str(normalised_location["candidates"][0]["formatted_address"]).lower()
                except KeyError:
                    self.debug("Normalisation failed, saving {} with undefined location.".format(user.username), 3)
                    return False

                # Couldn't think of a better way as the address is returned as a string with 2 formats for the state
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
                    user.state = "SA"
                elif "australia" in user.normalised_location:
                    # This special case is when the users location is just Australia. (ie no state etc specified)
                    # We're still interested in it because it's extra data for the national sentiment analysis.
                    user.state = "UNKNOWN"
                else:
                    # If we hit this statement they're almost certainly a fictional or international location.
                    user.state = "INTERNATIONAL"

                self.debug("found new user from {}".format(user.state), 1)

                # Save and return our user instance.
                user.save()
                return user

            else:
                # We couldn't normalise a location but leave the user anyway so we don't process them next time.
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

        # Process the username (add to db if not there, otherwise get instance).
        self.debug("attempting to process user: " + result.user.screen_name, 2)
        user = self.process_user(result)

        if not user:
            return False

        # Create a new tweet, or return the model instance if it exists.
        tweet = my_models.Tweet.get_or_create(snowflake=result.id, user_id=user.username)

        # If a new tweet was created add the data, save it then return it.
        if tweet[1]:
            tweet = tweet[0]
            tweet.user = user
            tweet.text = result.full_text
            tweet.likes = result.favorite_count
            tweet.retweets = result.retweet_count
            tweet.save()

            self.debug("saved tweet to db", 1)
            return True

        # If the tweet already exists, just exit.
        else:
            self.debug("tweet already exists in db", 2)
            return False

    def analyse_tweet_sentiment(self, tweet):
        """
        This method will run Microsoft sentiment analysis on the tweet and return the result.
        :param tweet:
        :return float:
        """

        # Payload to be sent to the Microsoft API. It's not batched because they count each individual "document" as
        # a separate transaction anyway.
        payload = {
            "documents": [
                {
                    "language": "en",
                    "id": "1",
                    "text": tweet.full_text
                }]
        }

        tweet = my_models.Tweet.get_by_id(tweet.id)

        try:
            # Run our sentiment analysis on the tweet and save the result to the database. TODO: Make this more robust.
            self.debug("attempting to run sentiment analysis on: " + tweet.text.strip(), 3)
            sentiment = requests.post(self.microsoft_api, data=json.dumps(payload), headers=self.microsoft_headers).json()
            print(sentiment)
            tweet.sentiment = sentiment["documents"][0]["score"]
            tweet.save()
            self.debug("sentiment analysis complete: " + str(tweet.sentiment), 2)
            return True

        except Exception:
            return False

    def scrape_twitter(self):
        """
        This method utilises the Twitter API and searches for tweats that match any of the defined tags.
        :return:
        """
        self.debug(datetime.datetime.now().strftime('%H:%M:%S') + " - scraping twitter", 1)
        search_term = ""

        # Generate the search phrase from our list of tags we're interested in.
        for x, tag in enumerate(self.follow_tags):
            if x == 0:
                search_term += tag["tag"]
            else:
                search_term += " OR " + tag["tag"]

        search_term += " -filter:retweets"

        # This one has no geolocation boundaries, so occasionally you get international/fictional locations.
        tweets = self.api.GetSearch(term=search_term, lang="en", result_type="mixed", include_entities=True, count=100)

        # This one guarantees Australian tweets, but it returns much fewer results so use other one.
        # results = api.GetSearch(term="@billshortenmp OR @ScottMorrisonMP OR @PaulineHansonOz -filter:retweets",
        #                    max_id=models.Tweet.select().limit(1)[0].snowflake, geocode="-27.532239,134.597291,2200km",
        #                    lang="en", result_type="mixed", include_entities=True, count=10)

        for tweet in tweets:
            # Attempt to add the tweet. If successful, then run sentiment analysis on it.
            if self.add_tweet(tweet):
                if self.analyse_tweet_sentiment(tweet):
                    self.debug("created user, added tweet and analysed it: " + str(tweet.full_text).rstrip(), 1)
