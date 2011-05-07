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
import healer

class CamperMissingDataForm(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates', 'update_missing_data.html')
        camper = db.get(self.request.get('camper_key'))
        self.response.out.write(template.render(path, {'camper' : camper}))

    def post(self):
        camper = db.get(self.request.get('camper_key'))
        camper.transportation_means = self.request.get('transportation_means')
        camper.bringing_rv = self.request.get('bringing_rv') == 'on'
        camper.rv_info = self.request.get('rv_info')
        camper.rv_hookup = self.request.get('rv_hookup') == 'on'
        camper.structure_info = self.request.get('structure_info')
        camper.food_type = self.request.get('food_type')
        camper.eats_beef = self.request.get('eats_beef') == 'on'
        camper.eats_chicken = self.request.get('eats_chicken') == 'on'
        camper.eats_pork = self.request.get('eats_pork') == 'on'
        camper.eats_bacon = self.request.get('eats_bacon') == 'on'
        camper.eats_fish = self.request.get('eats_fish') == 'on'
        camper.eats_tofu = self.request.get('eats_tofu') == 'on'
	camper.put()
	self.response.out.write('Thanks!')

class CamperEditForm(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates', 'edit_camper.html')
        conf = camp.current()
	camper = db.get(self.request.get('camper_key'))
	dates = campdate.SortedDates()
	healer = None
 	for h in camper.healer_set:
  	  healer = h	
        self.response.out.write(template.render(path, {'conf' : conf, 'camper' : camper, 'healer' : healer, 'dates' : dates}))

    def post(self):
	logging.info('"'+self.request.get('camper_key')+'"')		
	camper = db.get(self.request.get('camper_key'))    
	camper.realname = self.request.get('realname')
	camper.playaname = self.request.get('playaname')
	camper.email = self.request.get('email')
	camper.address = self.request.get('address')
	camper.returning = self.request.get('returning') == 'on'
	camper.years_as_heebee = self.request.get('years_as_heebee')
	camper.previous_camps = self.request.get('previous_camps')
	camper.default_world_job = self.request.get('default_world_job')
	camper.why_heebees = self.request.get('why_heebees')
	camper.story = self.request.get('story')
	camper.assigned_committee = self.request.get('assigned_committee')
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
	camper.bringing_rv = self.request.get('bringing_rv') == 'on'
	camper.rv_hookup = self.request.get('rv_hookup') == 'on'
	camper.rv_info = self.request.get('rv_info')
	camper.dorm_tent = self.request.get('dorm_tent') == 'on'
	camper.structure_info = self.request.get('structure_info')
	camper.food_type = self.request.get('food_type')
	camper.eats_beef = self.request.get('eats_beef') == 'on'
	camper.eats_chicken = self.request.get('eats_chicken') == 'on'
	camper.eats_pork = self.request.get('eats_pork') == 'on'
	camper.eats_bacon = self.request.get('eats_bacon') == 'on'
	camper.eats_fish = self.request.get('eats_fish') == 'on'
	camper.eats_tofu = self.request.get('eats_tofu') == 'on'
	camper.eats_human = self.request.get('eats_human') == 'on'
	camper.dietary_restrictions = self.request.get('dietary_restrictions')
    	camper.put()
	if self.request.get('healer_key'):
	  healer = db.get(self.request.get('healer_key'))
	  healer.modalities = self.request.get('modalities')
	  healer.certifications = self.request.get('certifications')
	  healer.professional = self.request.get('professional') == 'on'
	  healer.years_as_healer = int(self.request.get('years_as_healer'))
	  healer.tables_bringing = int(self.request.get('tables_bringing'))
	  healer.triage = self.request.get('triage') == 'on'
	  healer.preferred_time_to_heal = self.request.get('preferred_time_to_heal')
	  healer.inappropriate_response = self.request.get('inappropriate_response')
	  healer.suggested_qualifications = self.request.get('suggested_qualifications')
	  healer.put()
	
	self.redirect('/camper/edit?camper_key=' + self.request.get('camper_key'))

application = webapp.WSGIApplication(
    [
        ('/camper/edit', CamperEditForm),
        ('/camper/update_missing_data', CamperMissingDataForm)
        ],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
