import sys
import os

third_party = os.path.join(os.path.dirname(__file__), 'third_party')
sys.path.append(third_party)

# Include twilio
sys.path.append(os.path.join(third_party, 'twilio'))
# https://developers.google.com/appengine/docs/python/tools/appstats?csw=1
appstats_CALC_RPC_COSTS = True

def webapp_add_wsgi_middleware(app):
      from google.appengine.ext.appstats import recording
      app = recording.appstats_wsgi_middleware(app)
      return app
