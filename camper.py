from google.appengine.ext import db

class Camper(db.Model):
    name = db.StringProperty()
