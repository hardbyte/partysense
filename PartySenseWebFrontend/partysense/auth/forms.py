from registration_email.forms import EmailRegistrationForm
from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div, Field, MultiField, Submit, HTML, Hidden

CustomEmailRegistrationForm = EmailRegistrationForm

CustomEmailRegistrationForm.helper = FormHelper()
CustomEmailRegistrationForm.helper.add_input(Submit('submit', 'Register your account', css_class="btn-block"))


