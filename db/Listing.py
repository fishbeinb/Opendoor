from google.appengine.ext import ndb

class Listing(ndb.Model):
    listing_id = ndb.IntegerProperty(required=True)
    street = ndb.StringProperty()
    status = ndb.StringProperty(choices=["pending","active","sold"])
    price = ndb.IntegerProperty(indexed=True)
    bedrooms = ndb.IntegerProperty(indexed=True)
    bathrooms = ndb.IntegerProperty(indexed=True)
    sq_ft = ndb.IntegerProperty()
    lat = ndb.FloatProperty()#Or just use GeoPtProperty
    lng = ndb.FloatProperty()

    @classmethod
    def unique_properties(cls):
        return ['listing_id']
