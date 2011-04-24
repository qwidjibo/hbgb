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
import camper

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

class CampersAdminPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates', 'admin_campers.html')
        conf = camp.current()
        campers = db.GqlQuery('SELECT * FROM Camper')
        registered_campers = []
        accepted_campers = []
        waitlisted_campers = []
        rejected_campers = []
        for camper in campers:
            logging.error(camper.status)
            if camper.status == 'registered':
                logging.error('got ' + camper.status)
                registered_campers.append(camper)
            if camper.status == 'accepted':
                logging.error('got ' + camper.status)
                accepted_campers.append(camper)
            if camper.status == 'rejected':
                logging.error('got ' + camper.status)
                rejected_campers.append(camper)
            if camper.status == 'waitlisted':
                logging.error('got ' + camper.status)
                waitlisted_campers.append(camper)            

        self.response.out.write(template.render(path, {'conf' : conf, 
                                                       'registered_campers' : registered_campers,
                                                       'accepted_campers' : accepted_campers,
                                                       'rejected_campers' : rejected_campers,
                                                       'waitlisted_campers' : waitlisted_campers
                                                       }))

class CamperEditStatusFormSubmit(webapp.RequestHandler):
    def post(self):
        conf = camp.current()
        camper = db.get(self.request.get('key'))
        camper.status = self.request.get('status')
        camper.put()        
        self.redirect('/admin/campers')

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

class CommitteeAssignmentPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates', 'admin_committee_assignments.html')
        conf = camp.current()
        campers = db.GqlQuery('SELECT * FROM Camper WHERE status=\'accepted\'')
        unassigned_campers = []
        assigned_campers = {}
        for committee in conf.committees:
            assigned_campers[committee] = []
        for camper in campers:
            if not camper.assigned_committee:
                unassigned_campers.append(camper)
            else:
              if camper.assigned_committee in assigned_campers: 
	  	assigned_campers[camper.assigned_committee].append(camper)
	      else:
	        unassigned_campers.append(camper)

        template_vars = { 'conf' : conf,
                          'unassigned_campers' : unassigned_campers,
                          'assigned_campers' : assigned_campers}
#        for (committee, campers) in assigned_campers.items();
#          template_vars[committee] = campers
        self.response.out.write(template.render(path, template_vars))

    def post(self):
        conf = camp.current()
        camper = db.get(self.request.get('key'))
        camper.assigned_committee = self.request.get('assigned_committee')
        camper.put()        
        self.redirect('/admin/committeeassigner')


application = webapp.WSGIApplication(
    [
        ('/admin', LandingPage),
        ('/admin/camp', CampAdminPage),
        ('/admin/campers', CampersAdminPage),
        ('/admin/camper/editstatus', CamperEditStatusFormSubmit),
        ('/admin/committeeassigner', CommitteeAssignmentPage),
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
