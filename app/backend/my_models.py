from peewee import *
from playhouse.pool import PooledMySQLDatabase
import os

# All of these environment variables are needed to run.
needed_vars = (
    "DB_USERNAME",
    "DB_PASSWORD"
)

# Check if all of the environment variables exist and raise an exception if any of them don't.
# for var in needed_vars:
#     if var not in os.environ:
#         raise RuntimeError("Missing environment variable: " + var)

db = PooledMySQLDatabase("CAB432data", max_connections=100, stale_timeout=10, host="cab432-cluster.cluster-ro-cwi2bksacgtt.ap-southeast-2.rds.amazonaws.com", port=3306, user="root", passwd="DD0f93Nfs7EM")

# db = SqliteDatabase('hated.db') # un comment to use sqlite

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
    username = CharField(primary_key=True)  # twitter username
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
    snowflake = CharField(primary_key=True)
    user = ForeignKeyField(User)
    text = TextField(null=True)
    likes = IntegerField(default=0)
    retweets = IntegerField(default=0)
    sentiment = DoubleField(default=None, null=True)
    emotional_analysis = TextField(default=None, null=True)
    created_date = DateTimeField(default=None, null=True)

    class Meta:
        database = db


class Tag(Model):
    """
    Fields for reference: snowflake, username, text, likes, retweets, location, sentiment, emotional_analysis, created_date
    This is the tweet model for storing the individual tweets.
    """
    tag = TextField()
    image = TextField()
    displayname = TextField()

    class Meta:
        database = db