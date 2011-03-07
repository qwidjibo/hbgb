# just loads templates/index.html

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import camp

class HomePage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')        
        conf = camp.current()
        self.response.out.write(template.render(path, { 'conf' : conf }))

class StaticTemplate(webapp.RequestHandler):
    def get(self):
        path_lst = self.request.path.split('/')
        path_lst.reverse()
        path_lst.append('templates')
        path_lst.append(os.path.dirname(__file__))
        path_lst.reverse()
        path = os.sep.join(path_lst)
        conf = camp.current()
        self.response.out.write(template.render(path, { 'conf' : conf }))


application = webapp.WSGIApplication(
    [
        ('/', HomePage),
        ('/.*html', StaticTemplate)
        ],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


