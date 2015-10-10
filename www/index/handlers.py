from www.base.handlers import BaseHandler
from db.Listing import Listing
import urllib2
import csv
import logging
from geojson import Feature, Point, FeatureCollection

class IndexHandler(BaseHandler):
    def get(self):
        self.write("Hey, this is a very simple writeup, I used google app engine. I used a template I've used befor for some small projects. Overall this took me a little over an hour to code up. Not much to say other than that. I could have used something else, but Google app engine datastore makes this stuff super easy.")

#Very simple, all local
class ListingsHandler(BaseHandler):
    def get(self):
        min_max_params = {'price': 'price', 'bed': 'bedrooms', 'bath': 'bathrooms'}

        q = Listing.query()

        for p in min_max_params:
            try:#Will only fail if self.request.get("max_" + p) is not an int
                max_param = int(self.request.get("max_" + p))
                q = q.filter(getattr(Listing, min_max_params[p]) <= max_param)
            except:
                pass
            try:#Will only fail if self.request.get("max_" + p) is not an int
                min_param = int(self.request.get("min_" + p))
                q = q.filter(getattr(Listing, min_max_params[p]) >= min_param)
            except:
                pass

        valid_buildings = q.fetch()
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