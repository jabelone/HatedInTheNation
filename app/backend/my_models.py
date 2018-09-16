from peewee import *

db = SqliteDatabase('hated.db')

class User(Model):
    """
    Fields for reference: username, raw_location, normalised_location, state
    Our user model. For each tweet we come across the account details are stored.
    """
    STATES = (
        ("WA", "Western Australia"),
        ("NT", "Northern Territory"),
        ("SA", "South Australia"),
        ("QLD", "Queensland"),
        ("NSW", "New South Wales"),
        ("VIC", "Victoria"),
        ("TAS", "Tasmania"),
        ("ACT", "Australian Capitol Territory"),
    )
    username = TextField(primary_key=True)  # twtitter username
    raw_location = TextField(default=None, null=True) # their raw location, as set on their profile
    normalised_location = TextField(default=None, null=True) # the normalised location, as provided by the Google API
    state = TextField(default=None, choices=STATES, null=True) # the parsed state extracted from the normalised location

    class Meta:
        database = db

class Tweet(Model):
    """
    Fields for reference: snowflake, username, text, likes, retweets, location, sentiment, emotional_analysis, created_date
    This is the tweet model for storing the individual tweets.
    """
    snowflake = IntegerField(primary_key=True)
    user = ForeignKeyField(User)
    text = TextField(null=True)
    likes = IntegerField(default=0)
    retweets = IntegerField(default=0)
    sentiment = DoubleField(default=None, null=True)
    emotional_analysis = TextField(default=None, null=True)
    created_date = DateTimeField(default=None, null=True)

    class Meta:
        database = db
