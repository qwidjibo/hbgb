from google.appengine.ext import db
from google.appengine.ext.webapp import template

from google.appengine.ext.db import djangoforms

class Camper(db.Model):
    status = db.StringProperty(
        required=True,
        choices=[
            'new',
            'registered',
            'accepted',
            'rejected',
            'waitlisted'
            ],
        default='new')
    realname = db.StringProperty()
    playaname = db.StringProperty()
    email = db.EmailProperty()
    phone = db.PhoneNumberProperty()
    address = db.PostalAddressProperty()
    returning = db.BooleanProperty()

    years_as_heebee = db.StringProperty()
    previous_camps = db.TextProperty()
    burns = db.IntegerProperty()
    default_world_job = db.TextProperty()
    why_heebees = db.TextProperty()
    story = db.TextProperty()
    
    first_choice_committee = db.StringProperty()
    second_choice_committee = db.StringProperty()
    first_choice_reason = db.TextProperty()
    second_choice_reason = db.TextProperty()

    wants_to_heal = db.BooleanProperty()
    wants_to_teach = db.BooleanProperty()
    wants_to_lead = db.BooleanProperty()
    teaching_info = db.TextProperty()
    
    early_team = db.BooleanProperty()
    strike = db.BooleanProperty()

    arrival_date = db.StringProperty()
    departure_date = db.StringProperty()

    arrival_time = db.StringProperty(
        choices=['before_breakfast',
                 'before_lunch',
                 'before_dinner',
                 'after_dinner'])

    departure_time = db.StringProperty(
        choices=['before_breakfast',
                 'before_lunch',
                 'before_dinner',
                 'after_dinner'])

    transportation_means = db.StringProperty()
    
    bringing_rv = db.BooleanProperty()
    rv_hookup = db.BooleanProperty()
    rv_info = db.TextProperty()

    dorm_tent = db.BooleanProperty()
    structure_info = db.TextProperty()

    food_type = db.StringProperty(
        choices=['omnivore',
                 'pescatarian',
                 'vegitarian',
                 'vegan',
                 'raw'])

    eats_beef = db.BooleanProperty()
    eats_chicken = db.BooleanProperty()
    eats_pork = db.BooleanProperty()
    eats_bacon = db.BooleanProperty()
    eats_fish = db.BooleanProperty()
    eats_tofu = db.BooleanProperty()
    eats_human = db.BooleanProperty()

    dietary_restrictions = db.TextProperty()

    photo = db.BlobProperty()
    
