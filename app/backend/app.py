# Main "entry point" for CAB432 Assessment (individual project)
# Most of the twitter scraping/parsing logic is in twitter_logic.py and db models are in my_models.py.
# Student Name: Jaimyn Mayer (n9749331)

from flask import Flask, render_template, jsonify
from random import *
from flask_cors import CORS
import twitter_logic as t
import my_models
from peewee import *
from operator import itemgetter

# This will create the db if it doesn't exist but won't overrite it if it already does.
my_models.db.create_tables([my_models.Tweet, my_models.User])

app = Flask(__name__,
            static_folder="../dist/static",
            template_folder="../dist",
            )

# CORS config - allow our API to be accessed from other domains. TODO: Turn off in production.
cors = CORS(app, resources={r"/api/*": {"origins": "*"}, r"/crontab/*": {"origins": "*"}})

# This is a list of tags to follow and enter into the system. This list is hardcoded because the API for sentiment
# analysis is severely restricted as we only get 5000 tweets per month.
follow_tags = [
    {
        "tag": "@billshortenmp",  # Twitter tag to follow/search for.
        "image": "/static/images/billshorten.jpg",  # Link to an image of the tag.
        "displayname": "Lil Billy Shorten"  # The friendly name displayed in the UI.
    },
    {
        "tag": "@ScottMorrisonMP",
        "image": "/static/images/scottmorrison.png",
        "displayname": "Scott (Coal) Morrison"
    },
    {
        "tag": "@PaulineHansonOz",
        "image": "/static/images/paulinehanson.jpeg",
        "displayname": "Pauline Pantsdown"
    },
    {
        "tag": "@TonyAbbottMHR",
        "image": "/static/images/tonyabbot.jpg",
        "displayname": "Tony (Onion) Abbot"
    },
]


# Create a new instance of our twitter scraping class and give it our tags from above. Here we're setting the debug
# level to 3. Set to 0 for no output or 1, 2 ot 3 for increasing levels of verbosity.
twitter = t.TwitterScraper(follow_tags, 3)


@app.route('/api/random')
def random_number():
    """
    Generates a random number. For testing purposes.
    :return:
    """
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)


@app.route('/api/tweets')
def get_tweets():
    """
    This endpoint is used to fetch a list of every tweet that is in the database so we can show it on the UI.
    :return:
    """
    tweets = []

    # For every tweet in the database, add it to our list to send to the front end.
    for tweet in my_models.Tweet.select():
        if tweet.sentiment is None:
            # This shouldn't be possible, but let's handle it anyway
            continue


        tweets.append({
            "snowflake": tweet.snowflake,
            "text": tweet.text,
            "sentiment": round(tweet.sentiment * 100),
            "user": tweet.user.username,
            "state": tweet.user.state,
            "likes": tweet.likes,
            "retweets": tweet.retweets
        })

    # Return our list of tweets as a JSON response.
    return jsonify({'tweets': tweets})


@app.route('/api/tags')
def get_tags():
    """
    Gets a list of tags we're currently following, their image/display name and sentiment statistics if available.
    :return:
    """
    tag_data = []

    for tag in follow_tags:
        # Grab a list of all tweets the tag is mentioned in.
        tweets = my_models.Tweet.select().join(my_models.User).where(my_models.Tweet.text.contains(tag["tag"]))

        # Calculate the minimum sentiment.
        minimum = tweets.select(fn.Min(my_models.Tweet.sentiment)).scalar()
        if minimum:
            minimum = round(minimum * 100)
        else:
            minimum = 0

        # Calculate the maximum sentiment.
        maximum = tweets.select(fn.Max(my_models.Tweet.sentiment)).scalar()
        if maximum:
            maximum = round(maximum * 100)
        else:
            maximum = 0

        # Calculate the average sentiment.
        avg = tweets.select(fn.AVG(my_models.Tweet.sentiment)).scalar()
        if avg:
            avg = round(avg * 100)
        else:
            avg = 0

        data = {
            "tag": tag["tag"],
            "image": tag["image"],
            "displayname": tag["displayname"],
            "min": minimum,
            "max": maximum,
            "average": avg,
            "count": tweets.count(),
        }
        tag_data.append(data)

    # Return our list of tags, pre sorted by average sentiment so it's less work to display them on the front end.
    list = sorted(tag_data, key=itemgetter('average'))
    for x, item in enumerate(list):
        item["place"] = x+1

    return jsonify(list)


@app.route('/api/sentiment/')
def sentiment_data():
    """
    Gets a full list of all the sentiment data we have. Broken down by national, state and per tag statistics.
    :return:
    """
    state_data = {}  # All of our state statistics will be stored here.
    tag_data = {}  # All of the followed tag statistics will be stored here.
    states = ("QLD", "NSW", "VIC", "ACT", "TAS", "SA", "NT", "WA")  # For convenience later on.

    # Time to process all of followed tags.
    for tag in follow_tags:
        # Get a list of all tweets the tag is mentioned in.
        tweets = my_models.Tweet.select().join(my_models.User).where(my_models.Tweet.text.contains(tag["tag"]))

        # Calculate the minimum sentiment.
        minimum = tweets.select(fn.Min(my_models.Tweet.sentiment)).scalar()
        if minimum:
            minimum = round(minimum * 100)
        else:
            minimum = 0

        # Calculate the maximum sentiment.
        maximum = tweets.select(fn.Max(my_models.Tweet.sentiment)).scalar()
        if maximum:
            maximum = round(maximum * 100)
        else:
            maximum = 0

        # Calculate the average sentiment.
        avg = tweets.select(fn.AVG(my_models.Tweet.sentiment)).scalar()
        if avg:
            avg = round(avg * 100)
        else:
            avg = 0

        data = {
            "tag": tag["tag"],
            "image": tag["image"],
            "displayname": tag["displayname"],
            "min": minimum,
            "max": maximum,
            "average": avg,
            "count": tweets.count(),
        }

        # Store it in a dictionary accessible via the tag. Makes it easier on the front end.
        tag_data[tag["tag"]] = data

    # Time to process all of our states.
    for state in states:
        # Get a list of all tweets from the state.
        tweets = my_models.Tweet.select().join(my_models.User).where(my_models.Tweet.user.state == state)

        # Generate a list with the number of tweets each followed tag has in this state.
        tags = []
        for x, tag in enumerate(follow_tags):
            amount = tweets.select(fn.AVG(my_models.Tweet.sentiment)).where(my_models.Tweet.text.contains(tag["tag"]))
            amount = amount.scalar()

            if amount:
                amount = round(amount * 100)
            else:
                amount = 0

            tags.append((tag, amount))

        # Calculate the minimum sentiment.
        minimum = tweets.select(fn.Min(my_models.Tweet.sentiment)).scalar()
        if minimum:
            minimum = round(minimum * 100)
        else:
            minimum = 0

        # Calculate the maximum sentiment.
        maximum = tweets.select(fn.Max(my_models.Tweet.sentiment)).scalar()
        if maximum:
            maximum = round(maximum * 100)
        else:
            maximum = 0

        # Calculate the average sentiment.
        avg = tweets.select(fn.AVG(my_models.Tweet.sentiment)).scalar()
        if avg:
            avg = round(avg * 100)
        else:
            avg = 0

        data = {
            "name": state,
            "min": minimum,
            "max": maximum,
            "average": avg,
            "count": tweets.count(),
            "tags": sorted(tags, key=itemgetter(1))
        }
        state_data[state] = data

    # Calculate the average sentiment for all tweets from every tag/location.
    avg = my_models.Tweet.select(fn.AVG(my_models.Tweet.sentiment)).scalar()
    if avg:
        avg = round(avg * 100)
    else:
        avg = 0

    overall_data = {
        "average": avg,
        "count": my_models.Tweet.select().count(),
    }

    # Return a JSON list with the national/overall, followed tag and state statistics.
    return jsonify({"overall": overall_data, "tags": tag_data, "states": state_data})


@app.route('/crontab/twitter')
def crontab_twitter():
    """
    This is a way to trigger scraping new tweets from the front end UI. TODO: Add rate limiting.
    :return:
    """
    twitter.scrape_twitter()  # Scrape data :)

    response = {
        'success': True
    }

    # Tell the frontend we're done.
    return jsonify(response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Default catch all path for vue.js routing purposes.
    return render_template("index.html")
