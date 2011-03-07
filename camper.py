from google.appengine.ext import db
from google.appengine.ext.webapp import template

from google.appengine.ext.db import djangoforms

class Camper(db.Model):
    status = db.StringProperty(
        required=True,
        choices=[
            'new',
            'registered'
            ],
        default='new')
    realname = db.StringProperty()
    playaname = db.StringProperty()
    email = db.EmailProperty()
    phone = db.PhoneNumberProperty()
    address = db.PostalAddressProperty()
    returning = db.BooleanProperty()

    years_as_heebee = db.StringProperty()
    previous_camps = db.TextProperty()
    burns = db.IntegerProperty()
    default_world_job = db.TextProperty()
    why_heebees = db.TextProperty()
    story = db.TextProperty()
    
