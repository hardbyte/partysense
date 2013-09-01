from registration_email.forms import EmailRegistrationForm
from django import forms

CustomEmailRegistrationForm = EmailRegistrationForm

# If we want to get the first name as well...
# class CustomEmailRegistrationForm(EmailRegistrationForm):
#     pass#first_name = forms.CharField()


