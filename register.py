import cgi
import os
import Cookie

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import campdate
import camper
import camp
import healer

class LandingPage(webapp.RequestHandler):
    def get(self):
        conf = camp.current()
        if conf.reg_open:
            c = camper.Camper()
            c.put()
            self.response.headers.add_header('Set-Cookie', '_camper_key=%s' % (c.key()))
        
            path = os.path.join(os.path.dirname(__file__), 'templates', 'reg_landing.html')
            self.response.out.write(template.render(path, {'camp' : conf }))
        else:
            path = os.path.join(os.path.dirname(__file__), 'templates', 'reg_closed.html')
            self.response.out.write(template.render(path, {'camp' : conf }))
            

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
        conf = camp.current()
        camper = db.get(self.request.cookies['_camper_key'])
        path = os.path.join(os.path.dirname(__file__), 'templates', 'reg_personalinfo.html')
        self.response.out.write(template.render(path, { 'camper' : camper, 'camp' : conf }))

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
        self.redirect('/register/playainfo')

class PlayaInfoPage(webapp.RequestHandler):
    def get(self):
        conf = camp.current()
        camper = db.get(self.request.cookies['_camper_key'])
        
        path = os.path.join(os.path.dirname(__file__), 'templates', 'reg_playainfo.html')
        self.response.out.write(template.render(path, { 'camper' : camper, 'camp' : conf }))

    def post(self):
        camper = db.get(self.request.cookies['_camper_key'])
        camper.first_choice_committee = self.request.get('first_choice_committee')
        camper.second_choice_committee = self.request.get('second_choice_committee')
        camper.first_choice_reason = self.request.get('first_choice_reason')
        camper.second_choice_reason = self.request.get('second_choice_reason')
        camper.wants_to_heal = self.request.get('wants_to_heal') == 'on'
        camper.wants_to_teach = self.request.get('wants_to_teach') == 'on'
        camper.wants_to_lead = self.request.get('wants_to_lead') == 'on'
        camper.teaching_info = self.request.get('teaching_info')
        camper.early_team = self.request.get('early_team') == 'on'
        camper.strike = self.request.get('strike') == 'on'
        camper.arrival_date = self.request.get('arrival_date')
        camper.departure_date = self.request.get('departure_date')
        camper.arrival_time = self.request.get('arrival_time')
        camper.departure_time = self.request.get('departure_time')
        camper.transportation_means = self.request.get('transportation_means')
        bringing_rv = self.request.get('bringing_rv')
        rv_hookup = self.request.get('rv_hookup')
        rv_info = self.request.get('rv_info')
        dorm_tent = self.request.get('dorm_tent') == 'on'
        structure_info = self.request.get('structure_info')
        food_type = self.request.get('food_type')
        eats_beef = self.request.get('eats_beef') == 'on'
        eats_chicken = self.request.get('eats_chicken') == 'on'
        eats_pork = self.request.get('eats_pork') == 'on'
        eats_bacon = self.request.get('eats_bacon') == 'on'
        eats_fish = self.request.get('eats_fish') == 'on'
        eats_tofu = self.request.get('eats_tofu') == 'on'
        eats_human = self.request.get('eats_human') == 'on'
        dietary_restrictions = self.request.get('dietary_restrictions')
        camper.put()

        self.redirect('/register/dates')

class DateInfoPage(webapp.RequestHandler):
    def get(self):
        conf = camp.current()
        camper = db.get(self.request.cookies['_camper_key'])
        path = os.path.join(os.path.dirname(__file__), 'templates', 'reg_dates.html')

        early_dates = db.GqlQuery('SELECT * FROM CampDate WHERE early_team=TRUE ORDER BY date').fetch(100)
        dates = db.GqlQuery('SELECT * FROM CampDate WHERE early_team=FALSE ORDER BY date').fetch(100)
        strike_dates = db.GqlQuery('SELECT * FROM CampDate WHERE strike=TRUE ORDER BY date').fetch(100)

        self.response.out.write(template.render(path, { 'camper' : camper, 
                                                        'camp' : conf,
                                                        'early_dates' : early_dates,
                                                        'dates' : dates,
                                                        'strike_dates' : strike_dates }))

    def post(self):
        camper = db.get(self.request.cookies['_camper_key'])

        camper.early_team = self.request.get('early_team') == 'on'
        camper.strike = self.request.get('strike') == 'on'
        camper.arrival_time = self.request.get('arrival_time')
        camper.departure_time = self.request.get('departure_time')
        camper.arrival_date = self.request.get('arrival_date')
        camper.departure_date = self.request.get('departure_date')
        
        camper.put()
        if camper.wants_to_heal:
            self.redirect('/register/healerinfo')
        else:
            self.redirect('/register/photoupload')

class HealerInfoPage(webapp.RequestHandler):
    def get(self):
        conf = camp.current()
        camper = db.get(self.request.cookies['_camper_key'])
        path = os.path.join(os.path.dirname(__file__), 'templates', 'reg_healerinfo.html')
        self.response.out.write(template.render(path, { 'camper' : camper, 'camp' : conf }))

    def post(self):
        camper = db.get(self.request.cookies['_camper_key'])
        h = healer.Healer()
        h.camper = camper
        h.status = 'registered'
        h.modalities = self.request.get('modalities')
        h.certifications = self.request.get('certifications')
        h.professional = self.request.get('professional') == 'on'
        h.years_as_healer = int(self.request.get('years_as_healer'))
        h.tables_bringing = int(self.request.get('tables_bringing'))
        h.triage = self.request.get('triage') == 'on'
        h.preferred_time_to_heal = self.request.get('preferred_time_to_heal')
        h.inappropriate_response = self.request.get('inappropriate_response')
        h.suggested_qualifications = self.request.get('suggested_qualifications')
        h.put()
        self.redirect('/register/photoupload')

class PhotoUploadPage(webapp.RequestHandler):
    def get(self):
        conf = camp.current()
        camper = db.get(self.request.cookies['_camper_key'])
        path = os.path.join(os.path.dirname(__file__), 'templates', 'reg_photoupload.html')
        self.response.out.write(template.render(path, { 'camper' : camper, 'camp' : conf }))

    def post(self):
        camper = db.get(self.request.cookies['_camper_key'])
        camper.photo = db.Blob(self.request.get("photo"))
        camper.put()
        self.redirect('/register/confirm')

class ConfirmationPage(webapp.RequestHandler):
    def get(self):
        conf = camp.current()
        camper = db.get(self.request.cookies['_camper_key'])
        path = os.path.join(os.path.dirname(__file__), 'templates', 'reg_confirm.html')
        self.response.out.write(template.render(path, { 'camper' : camper, 'camp' : conf }))
        
application = webapp.WSGIApplication(
    [
        ('/register', LandingPage),
        ('/register/personalinfo', PersonalInfoPage),
        ('/register/playainfo', PlayaInfoPage),
        ('/register/dates', DateInfoPage),
        ('/register/healerinfo', HealerInfoPage),
        ('/register/photoupload', PhotoUploadPage),
        ('/register/confirm', ConfirmationPage)
        ],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
