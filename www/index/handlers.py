from www.base.handlers import BaseHandler
from db.Listing import Listing
import urllib2
import csv
from google.appengine.ext import ndb
import logging
from geojson import Feature, Point, FeatureCollection
from google.appengine.ext import ndb

class IndexHandler(BaseHandler):
    def get(self):
        self.write("Hey, this is a very simple writeup, I used google app engine. I used a template I've used befor for some small projects. Overall this took me a little over an hour to code up. Not much to say other than that. I could have used something else, but Google app engine datastore makes this stuff super easy. (In retrospect redis might have been better)")

#Very simple, all local
class ListingsHandler(BaseHandler):
    def get(self):
        qo = ndb.QueryOptions(keys_only=True)
        min_max_params = {'price': 'price', 'bed': 'bedrooms', 'bath': 'bathrooms'}
        query_sets = []
        #Should have just used redis :p
        for p in min_max_params:
            q = Listing.query()
            add_to_sets = False
            try:#Will only fail if self.request.get("max_" + p) is not an int
                max_param = int(self.request.get("max_" + p))
                q = q.filter(getattr(Listing, min_max_params[p]) <= max_param)
                add_to_sets = True
            except:
                pass
            try:#Will only fail if self.request.get("max_" + p) is not an int
                min_param = int(self.request.get("min_" + p))
                q = q.filter(getattr(Listing, min_max_params[p]) >= min_param)
                add_to_sets = True
            except:
                pass
            if add_to_sets:
                query_sets = query_sets + [set(q.fetch(keys_only=True))]

        if len(query_sets):
            valid_buildings = ndb.get_multi(list(set.intersection(*query_sets)))
        else:
            valid_buildings = Listing.query().fetch()
        
        all_features = []
        for b in valid_buildings:
            all_features = all_features + [Feature(geometry=Point((b.lat, b.lng)), 
                properties={"id": b.listing_id,
                "price": b.price,
                "street": b.street,
                "bedrooms": b.bedrooms,
                "bathrooms": b.bathrooms,
                "sq_ft": b.sq_ft
                })]
        self.write((FeatureCollection(all_features)))


#Commented out to avoid messing up the DB durring queue
#Did not use bulkloader, simple parsed and uploaded locally
"""
class PopulateHandler(BaseHandler):
    def get(self):
        response = urllib2.urlopen('https://s3.amazonaws.com/opendoor-problems/listings.csv')
        listings_csv = response.read()
        listings = csv.reader(listings_csv.split("\n")[1:-1], delimiter=',')
        for l in listings:
            logging.error(l)
            Listing(listing_id=int(l[0]),
                street=l[1],
                status=l[2],
                price=int(l[3]),
                bedrooms=int(l[4]),
                bathrooms=int(l[5]),
                sq_ft=int(l[6]),
                lat=float(l[7]),
                lng=float(l[8])
                ).put()
        self.write("Done")
"""