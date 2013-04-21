from django.db import models
from django.forms import ModelForm,  CharField, DateField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, Select, DateTimeInput, HiddenInput

from models import *
from widgets import GoogleMapsWidget


class EventForm(ModelForm):
    class Meta:
        model = Event

        # Explicitly specifying the fields we want
        fields = ('title',
                  'happening_now',
                  'start_time'
                  )

    # TODO default to next Saturday evening?
    start_time = DateField(widget=DateTimeInput(
        attrs={'class':'timepicker', 'type': 'datetime-local'})
    )

    address = CharField(label="Venue")
    latitude = CharField(widget = GoogleMapsWidget(
        attrs={'width': 800, 'height': 400, 'longitude_id':'id_longitude'}),
        error_messages={'required': 'Please select point from the map.'},
        help_text="location")

    longitude = CharField(widget = HiddenInput())


