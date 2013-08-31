from django.db import models
from django.forms import ModelForm, Textarea, IntegerField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, Select
from django.core.validators import validate_email

from models import *

class ClubForm(ModelForm):
    class Meta:
        model = Club
		
        # Explicitly specifying the fields we want
        fields = ('club_name',
                  'club_email',
                  'website',
                  'facebook_page',
                  'address',
                  'city',
                  'country')

        # @todo: Where does the user authentication happen? 

        widgets = {
            #'content': Textarea(attrs={'cols': 60, 'rows': 10}),
            }
