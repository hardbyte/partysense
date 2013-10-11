from registration_email.forms import EmailRegistrationForm
from registration_email.forms import EmailAuthenticationForm as OriginalEmailAuthenticationForm

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div, Field, MultiField, Submit, HTML, Hidden

CustomEmailRegistrationForm = EmailRegistrationForm
CustomEmailRegistrationForm.helper = FormHelper()
CustomEmailRegistrationForm.helper.add_input(Submit('submit', 'Register your account', css_class="btn-block"))


class EmailAuthenticationForm(OriginalEmailAuthenticationForm):
    def __init__(self, *args, **kwargs):

        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Login'))
