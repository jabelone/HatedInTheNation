# Some testing code for CAB432 Assessment (individual project)
# Student Name: Jaimyn Mayer (n9749331)

import time
import twitter_logic as t

follow_tags = [
    {
        "tag": "@billshortenmp",
        "profile": "/static/images/billshorten.jpg",
        "displayname": "Bill Shorten"
    },
    {
        "tag": "@ScottMorrisonMP",
        "profile": "/static/images/paulinehanson.jpeg",
        "displayname": "ScoMo"
    },
    {
        "tag": "@PaulineHansonOz",
        "profile": "/static/images/scottmorrison.png",
        "displayname": "Pauline Pantsdown"
    },
]

twitter = t.TwitterScraper(follow_tags, 1)

while True:
    # this will scrap tweets from the api, pull out users/locations, run sentiment analysis and save to our db
    twitter.scrape_twitter()

    # wait for a bit so we don't hit twitter's rate limit
    time.sleep(60)