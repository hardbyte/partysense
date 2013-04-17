from django.db import models
from django.forms import ModelForm, Textarea, IntegerField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, Select
from models import *


class EventForm(ModelForm):
    class Meta:
        model = Event

        # Explicitly specifying the fields we want
        fields = ('title',
                  'location',
                  'start_time',
                  'happening_now'
                  )

