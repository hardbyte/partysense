import datetime
from django.core.exceptions import ValidationError

from django.db import models
from django.forms import ModelForm,  CharField, SplitDateTimeField, DateInput, TimeInput
from django.forms.widgets import SplitDateTimeWidget, HiddenInput, MultiWidget

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div, Field

from models import *
from widgets import GoogleMapsWidget



class EventForm(ModelForm):
    class Meta:
        model = Event

        # Explicitly specifying the fields we want
        fields = ('title',
                  'user_editable',
                  'start_time'
                  )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-inline"
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-8"
        self.helper.layout = Layout('title',
                                    'user_editable',
                                    Div('start_time',
                                        css_class="col-lg-10")
        )

    start_time = SplitDateTimeField(
        input_date_formats=['%Y-%m-%d'],
        input_time_formats=['%H:%M'],
    )

    venue = CharField(label="Venue", widget=GoogleMapsWidget(
        attrs={
            'width': 800,
            'height': 400,
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

