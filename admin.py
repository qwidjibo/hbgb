import cgi
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
        conf.year = self.request.get('year')
        conf.put()


application = webapp.WSGIApplication(
    [
        ('/admin', LandingPage),
        ('/admin/camp', CampAdminPage)
        ],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
