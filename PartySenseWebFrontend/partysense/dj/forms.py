from django.db import models
from django.forms import ModelForm, Textarea, IntegerField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, Select
from django.core.validators import validate_email

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from partysense.dj.models import *

class DJForm(ModelForm):

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Register', css_class="btn-block"))

    class Meta:
        model = DJ

        # Explicitly specifying the fields we want
        fields = (
            'nickname',
            'email',
            'city_name',
            'url')

