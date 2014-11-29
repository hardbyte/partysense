from django.db import models
from django.forms import ModelForm, Textarea, IntegerField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, Select
from django.core.validators import validate_email

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from partysense.club.models import *


class NewClubForm(ModelForm):

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Register club', css_class="btn-block"))

    class Meta:
        model = Club
        fields = ("name", "email", "website", "facebook_page", "city", "country", "description")


