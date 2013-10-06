import datetime
from django.core.exceptions import ValidationError

from django.db import models
from django.forms import ModelForm,  CharField, SplitDateTimeField, DateInput, TimeInput
from django.forms.widgets import SplitDateTimeWidget, HiddenInput, MultiWidget

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div, Field, MultiField, Submit, HTML, Hidden

from models import *
from widgets import GoogleMapsWidget


class EventForm(ModelForm):
    class Meta:
        model = Event

        # Explicitly specifying the fields we want from the model
        fields = ('title',
                  'user_editable',
                  'start_time'
                  )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = "well"
        #self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('title'),
                    Div(
                         Field('user_editable', css_class="col-md-3"),
                         css_class="col-md-6"
                    ),
                    Div(Field('start_time'), css_class="col-md-6"),

                    css_class="col-md-6"),
                Div(Div(css_class="row"),
                    Div('venue', css_class="col-md-12"),
                    css_class="col-md-6"),
                css_class="row"),


            Div(css_class="row"),

            Field('latitude', css_id='id_latitude'),
            Field('longitude', css_id='id_longitude'),
            Div(Submit('submit', 'Submit', css_class="btn-block"),
                css_class="col-md-12")
        )

        #self.helper.add_input()

    start_time = SplitDateTimeField(
        input_date_formats=['%Y-%m-%d'],
        input_time_formats=['%H:%M'],
    )

    venue = CharField(label="Venue", widget=GoogleMapsWidget(
        attrs={
            'width': 800,
            'height': 300,
              }),
        error_messages={'required': 'Please select point from the map.'},
        help_text="location")

    latitude = CharField(widget=HiddenInput())
    longitude = CharField(widget=HiddenInput())

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        return cleaned_data

    def clean_title(self):
        words = self.cleaned_data['title'].split()

        if len(words) > 20 or any(len(w) > 17 for w in words):
            raise ValidationError("How about a shorter event name?")

        return " ".join(words)

    def clean_venue(self):
        if "venue" not in self.cleaned_data:
            raise ValidationError("Please provide a venue name or address")
        return self.cleaned_data['venue']

    def clean_start_time(self):
        date = self.cleaned_data['start_time'].date()
        logger.info("date: {}".format(date))
        if date < datetime.date.today():
            raise ValidationError("The date must be in the future!")
        return self.cleaned_data['start_time']

