from django import forms

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div, Field, MultiField, Submit, HTML, Hidden
from registration.forms import RegistrationForm


class CustomEmailRegistrationForm(RegistrationForm):

    username = None

    def __init__(self, *args, **kwargs):
        super(CustomEmailRegistrationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Register your account', css_class="btn-block"))


class EmailAuthenticationForm(forms.Form):

    username = forms.EmailField(
        label="Email Address",
        max_length=160,
        required=True,
    )

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):

        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Login'))
