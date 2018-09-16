# Main backend code for CAB432 Assessment (individual project)
# Student Name: Jaimyn Mayer (n9749331)

from flask import Flask, render_template, jsonify
from random import *
from flask_cors import CORS
import twitter_logic as t
import my_models

# This will create the db if it doesn't exist
my_models.db.create_tables([my_models.Tweet, my_models.User])

app = Flask(__name__,
            static_folder="../dist/static",
            template_folder="../dist",
            )

# CORS config
cors = CORS(app, resources={r"/api/*": {"origins": "*"}, r"/crontab/*": {"origins": "*"}})

follow_tags = [
    {
        "tag": "@billshortenmp",
        "image": "/static/images/billshorten.jpg",
        "displayname": "Bill Shorten"
    },
    {
        "tag": "@ScottMorrisonMP",
        "image": "/static/images/scottmorrison.png",
        "displayname": "ScoMo"
    },
    {
        "tag": "@PaulineHansonOz",
        "image": "/static/images/paulinehanson.jpeg",
        "displayname": "Pauline Pantsdown"
    },
]

twitter = t.twitter_scraper(follow_tags, 3)


@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)


@app.route('/api/tweets')
def get_tweets():
    tweets = []

    for tweet in my_models.Tweet.select():
        tweets.append({
            "snowflake": tweet.snowflake,
            "text": tweet.text,
            "sentiment": round(float(tweet.sentiment), 3),
            "user": tweet.user.username,
            "state": tweet.user.state,
            "likes": tweet.likes,
            "retweets": tweet.retweets
        })

    response = {
        'tweets': tweets
    }
    return jsonify(response)


@app.route('/api/tags')
def get_follow_tags():
    return jsonify(follow_tags)


@app.route('/api/sentiment/overall')
def overall_sentiment():
    query = my_models.Tweet.select().where(my_models.Tweet.active == True).order_by(my_models.Tweet.user)


@app.route('/crontab/twitter')
def crontab_twitter():
    # TODO: un comment this after development has finished, commented during dev due to API limits
    # twitter.scrape_twitter()

    response = {
        'complete': True
    }

    return jsonify(response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")
