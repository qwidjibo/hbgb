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
    email = db.StringProperty()
    



