from google.appengine.ext import db
from google.appengine.ext.webapp import template

class CampDate(db.Model):
    date = db.DateProperty(required=True)
    early_team = db.BooleanProperty(default=False)
    strike = db.BooleanProperty(default=False)
    desc = db.StringProperty(default="")


def SortedDates():
  q = db.GqlQuery('SELECT * FROM CampDate ORDER BY date ASC')
  dates = []
  for d in q.fetch(100):
    dates.append(d)
  return dates
