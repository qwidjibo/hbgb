from google.appengine.ext import db
from google.appengine.ext.webapp import template

class Camp(db.Model):
    reg_status = db.StringProperty(choices=['closed',
                                            'open'],
                                   required=True,
                                   default='closed')
    year = db.IntegerProperty(required=True,
                              default=1)

def current():
    camp = db.GqlQuery('SELECT * FROM Camp').get()
    if camp is None:
        camp = Camp()
        camp.put()
    return camp


