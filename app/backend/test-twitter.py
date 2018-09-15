# Some testing code for CAB432 Assessment (individual project)
# Student Name: Jaimyn Mayer (n9749331)

import time
import twitter_logic as t

twitter = t.twitter_scraper(1)

while True:
    # this will scrap tweets from the api, pull out users/locations, run sentiment analysis and save to our db
    twitter.scrape_twitter()

    # wait for a bit so we don't hit twitter's rate limit
    time.sleep(5)