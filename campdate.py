from google.appengine.ext import db

class CampDate(db.Model):
    date = db.DateProperty(required=True)
    eary_team = db.BooleanProperty(default=False)
    strike = db.BooleanProperty(default=False)
    desc = db.StringProperty(default="")

