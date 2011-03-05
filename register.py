import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import camper

class LandingPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""
          <html>
            <body>
              Welcome to the HeeBeeGeeBees! Please tell us your name.
              <form action="/register/create" method="post">
                <div><textarea name="content" rows="3" cols="60"></textarea></div>
                <div><input type="submit" value="Sign Up"></div>
              </form>
            </body>
          </html>""")


class CreateCamper(webapp.RequestHandler):
    def post(self):
        self.response.out.write('<html><body>Welcome to the camp, ')
        self.response.out.write(cgi.escape(self.request.get('content')))
        self.response.out.write('</body></html>')
        c = camper.Camper(name=cgi.escape(self.request.get('content')))
        self.response.out.write('writing ' + c.name + ' to the db.')
        c.put()


application = webapp.WSGIApplication(
                                     [('/register', LandingPage),
                                      ('/register/create', CreateCamper)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
