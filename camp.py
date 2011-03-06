from google.appengine.ext import db
from google.appengine.ext.webapp import template

class Camp(db.Model):
    reg_open = db.BooleanProperty(required=True,
                                  default=False)
    reg_closed_message = db.TextProperty()
    year = db.IntegerProperty(required=True,
                              default=1)
    base_dues = db.IntegerProperty(required=True,
                                   default=666)
    early_team_discount = db.IntegerProperty(required=True,
                                             default=100)
    strike_discount = db.IntegerProperty(required=True,
                                         default=50)

class CampDate(db.Model):
    date = db.DateProperty(required=True)
    eary_team = db.BooleanProperty(default=False)
    strike = db.BooleanProperty(default=False)
    desc = db.StringProperty(default="")

def current():
    camp = db.GqlQuery('SELECT * FROM Camp').get()
    if camp is None:
        camp = Camp()
        camp.put()
    return camp


