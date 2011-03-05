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

        self.redirect('/register/basicinfo')

class BasicInfoPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates', 'reg_basicinfo.html')
        self.response.out.write(template.render(path, { }))

    def post(self):
        camper = db.get(self.request.cookies['_camper_key'])
        camper.playaname = self.request.get('playaname')
        camper.put()
        self.redirect('/register/confirm')

class ConfirmationPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write('All done!')


application = webapp.WSGIApplication(
    [
        ('/register', LandingPage),
        ('/register/basicinfo', BasicInfoPage),
        ('/register/confirm', ConfirmationPage),
        ],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
