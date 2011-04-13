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
    modalities = db.StringProperty()
    certifications = db.StringProperty()
    professional = db.BooleanProperty()
    years_as_healer = db.IntegerProperty()
    tables_bringing = db.IntegerProperty()
    triage = db.BooleanProperty()
    preferred_time_to_heal = db.StringProperty(
          choices = [
            'morning',
            'midday',
            'afternoon'
          ])
    inappropriate_response = db.StringProperty()
    suggested_qualifications = db.StringProperty()
   
