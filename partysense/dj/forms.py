from django.db import models
from django.forms import ModelForm, Textarea, IntegerField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, Select
from django.core.validators import validate_email

from models import *

class DJForm(ModelForm):
    class Meta:
        model = DJ

        # Explicitly specifying the fields we want
        fields = ('email',
                  'nickname',
                  'city_name'
                )

        widgets = {
            #'content': Textarea(attrs={'cols': 60, 'rows': 10}),
            }
