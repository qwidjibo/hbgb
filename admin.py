import cgi
import logging
import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import camp

class LandingPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates', 'admin_landing.html')
        self.response.out.write(template.render(path, { }))

class CampAdminPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates', 'admin_camp.html')
        conf = camp.current()
        self.response.out.write(template.render(path, {'conf' : conf }))

    def post(self):
        conf = camp.current()
        conf.year = int(self.request.get('year'))
        conf.reg_open = self.request.get('reg_open') == 'on'
        conf.reg_closed_message = self.request.get('reg_closed_message')
        conf.base_dues = int(self.request.get('base_dues'))
        conf.early_team_discount = int(self.request.get('early_team_discount'))
        conf.strike_discount = int(self.request.get('strike_discount'))
        conf.put()
        self.redirect('/admin/camp')

class DatesAdminFormSubmit(webapp.RequestHandler):
    def post(self):
        self.redirect('/admin/camp')


application = webapp.WSGIApplication(
    [
        ('/admin', LandingPage),
        ('/admin/camp', CampAdminPage),
        ('/admin/dates', DatesAdminFormSubmit)
        ],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
