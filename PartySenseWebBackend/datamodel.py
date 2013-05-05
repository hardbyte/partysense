__author__ = 'robert'

from google.appengine.ext import ndb

class Club(ndb.Model):
    image_dict = ndb.PickleProperty()
    name = ndb.StringProperty(required=True)
    city = ndb.StringProperty()
    address = ndb.StringProperty()
    phone_number = ndb.StringProperty()
    email = ndb.StringProperty()
    website = ndb.StringProperty()
    twitter = ndb.StringProperty()
    facebook = ndb.StringProperty()
    google_plus = ndb.StringProperty()

    time_created = ndb.DateTimeProperty(auto_now_add=True)
    time_updated = ndb.DateTimeProperty(auto_now=True)

    latitude = ndb.FloatProperty()
    longitude = ndb.FloatProperty()

    images = ndb.BlobKeyProperty(repeated=True)
    banner_img = ndb.BlobKeyProperty()

    tags = ndb.StringProperty(repeated=True)

    description = ndb.TextProperty()

    unstructured_data = ndb.TextProperty()

    hours_default = ndb.StringProperty()
    hours_monday = ndb.StringProperty()
    hours_tuesday = ndb.StringProperty()
    hours_wednesday = ndb.StringProperty()
    hours_thursday = ndb.StringProperty()
    hours_friday = ndb.StringProperty()
    hours_saturday = ndb.StringProperty()
    hours_sunday = ndb.StringProperty()

class User(ndb.Model):
    name = ndb.StringProperty()
    age = ndb.StringProperty()
    email = ndb.StringProperty()
    clubs_favorite = ndb.StringProperty(repeated=True)
    clubs_visited = ndb.StringProperty(repeated=True)
    favorite_genres = ndb.StringProperty(repeated=True)
    friends_registered = ndb.KeyProperty(kind='User')
    friends_facebook = ndb.StringProperty(repeated=True)

    time_last_updated = ndb.DateTimeProperty() #time since last sync

    latitude = ndb.FloatProperty()
    longitude = ndb.FloatProperty()
    time_location_updated = ndb.DateTimeProperty()

    facebook_id = ndb.StringProperty()
    spotify_id = ndb.StringProperty()
    last_fm_id = ndb.StringProperty()

    profile_picture_blob_key = ndb.BlobKeyProperty()
    profile_picture_url = ndb.StringProperty()

class Tag(ndb.Model):
    tags = ndb.StringProperty(repeated=True)
    #underscore separated
    #e.g. [genre_hiphop, genre_dance, genre_pop, age_20-25, age_25-30]

class TrendingClubs(ndb.Model):
    clubs = ndb.KeyProperty(kind=Club, repeated=True)
