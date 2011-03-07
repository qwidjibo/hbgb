import cgi
import os
import Cookie

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import camper

class LandingPage(webapp.RequestHandler):
    def get(self):
        c = camper.Camper()
        c.put()
        self.response.headers.add_header('Set-Cookie', '_camper_key=%s' % (c.key()))
        
        path = os.path.join(os.path.dirname(__file__), 'templates', 'reg_landing.html')
        self.response.out.write(template.render(path, { }))

    def post(self):
        camper = db.get(self.request.cookies['_camper_key'])
        camper.realname = self.request.get('realname')
        camper.email = self.request.get('email')
        camper.playaname = self.request.get('playaname')
        camper.phone = self.request.get('phone')
        camper.address = self.request.get('address')
        camper.returning = self.request.get('returning') == 'on'
        camper.put()

        self.redirect('/register/personalinfo')

class PersonalInfoPage(webapp.RequestHandler):
    def get(self):
        camper = db.get(self.request.cookies['_camper_key'])
        path = os.path.join(os.path.dirname(__file__), 'templates', 'reg_personalinfo.html')
        self.response.out.write(template.render(path, { 'camper' : camper }))

    def post(self):
        camper = db.get(self.request.cookies['_camper_key'])
        if self.request.get('burns'):
            camper.burns = int(self.request.get('burns'))
        else:
            camper.burns = 0
        camper.years_as_heebee = self.request.get('years_as_heebee')
        camper.previous_camps = self.request.get('previous_camps')
        camper.default_world_job = self.request.get('default_world_job')
        camper.why_heebees = self.request.get('why_heebees')
        camper.story = self.request.get('story')
        camper.put()
        self.redirect('/register/confirm')

class ConfirmationPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write('All done!')


application = webapp.WSGIApplication(
    [
        ('/register', LandingPage),
        ('/register/personalinfo', PersonalInfoPage),
        ('/register/confirm', ConfirmationPage),
        ],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
