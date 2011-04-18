from google.appengine.ext import db
from google.appengine.ext.webapp import template

import camper

class Healer(db.Model):
    camper = db.ReferenceProperty(camper.Camper)
    status = db.StringProperty(
          choices=[
            'registered',
            'accepted',
            'rejected'
          ])
    modalities = db.TextProperty()
    certifications = db.TextProperty()
    professional = db.BooleanProperty()
    years_as_healer = db.IntegerProperty()
    tables_bringing = db.IntegerProperty()
    triage = db.BooleanProperty()
    preferred_time_to_heal = db.StringProperty(
          choices = [
            'morning',
            'midday',
            'afternoon',
            'evening'
          ])
    inappropriate_response = db.TextProperty()
    suggested_qualifications = db.TextProperty()
   
