import cgi
import datetime
import logging
import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import camp
import campdate

class LandingPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates', 'admin_landing.html')
        self.response.out.write(template.render(path, { }))

class CampAdminPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates', 'admin_camp.html')
        conf = camp.current()
        dates = db.GqlQuery('SELECT * FROM CampDate ORDER BY date')
        self.response.out.write(template.render(path, {'conf' : conf, 'dates' : dates}))

    def post(self):
        conf = camp.current()
        conf.year = int(self.request.get('year'))
        conf.reg_open = self.request.get('reg_open') == 'on'
        conf.reg_closed_message = self.request.get('reg_closed_message')
        conf.location_message = self.request.get('location_message')
        conf.base_dues = int(self.request.get('base_dues'))
        conf.early_team_discount = int(self.request.get('early_team_discount'))
        conf.strike_discount = int(self.request.get('strike_discount'))
        conf.early_pay_discount = int(self.request.get('early_pay_discount'))
        conf.reg_email_from = self.request.get('reg_email_from')
        conf.reg_email_subject = self.request.get('reg_email_subject')
        conf.reg_email_body = self.request.get('reg_email_body')
        conf.put()
        self.redirect('/admin/camp')

class DateAddFormSubmit(webapp.RequestHandler):
    def post(self):
        d = datetime.date(int(self.request.get('year')),
                          int(self.request.get('month')),
                          int(self.request.get('day')))
        cd = campdate.CampDate(date=d)
        cd.early_team = self.request.get('early_team') == 'on'
        cd.strike = self.request.get('strike') == 'on'
        cd.desc = self.request.get('desc')
        cd.put()

        self.redirect('/admin/camp')

class DateEditFormSubmit(webapp.RequestHandler):
    def post(self):
        cd = db.get(self.request.get('key'))
        cd.early_team = self.request.get('early_team') == 'on'
        cd.strike = self.request.get('strike') == 'on'
        cd.desc = self.request.get('desc')
        cd.put()

        self.redirect('/admin/camp')

class DateDeleteFormSubmit(webapp.RequestHandler):
    def post(self):
        db.delete(self.request.get('key'))
        self.redirect('/admin/camp')

class CommitteeAddFormSubmit(webapp.RequestHandler):
    def post(self):
        conf = camp.current()
        conf.committees.append(self.request.get('committee'))
        conf.put()
        self.redirect('/admin/camp')

class CommitteeDeleteFormSubmit(webapp.RequestHandler):
    def post(self):
        conf = camp.current()
        conf.committees.remove(self.request.get('committee'))
        conf.put()        
        self.redirect('/admin/camp')

application = webapp.WSGIApplication(
    [
        ('/admin', LandingPage),
        ('/admin/camp', CampAdminPage),
        ('/admin/dates/add', DateAddFormSubmit),
        ('/admin/dates/edit', DateEditFormSubmit),
        ('/admin/dates/delete', DateDeleteFormSubmit),
        ('/admin/committee/add', CommitteeAddFormSubmit),
        ('/admin/committee/delete', CommitteeDeleteFormSubmit)
        ],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
