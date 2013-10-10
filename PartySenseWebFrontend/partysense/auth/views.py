import logging

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from registration_email.forms import EmailAuthenticationForm as OriginalEmailAuthenticationForm


class EmailAuthenticationForm(OriginalEmailAuthenticationForm):
    def __init__(self, *args, **kwargs):

        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Login'))


def password_login(request):
    if request.method == 'POST':
        # Create a bound form
        auth_form = EmailAuthenticationForm(data=request.POST)
        logging.info("Authentication form valid? {}".format(auth_form.is_valid()))
        if auth_form.is_valid():
            logging.info("Email: {}".format(auth_form.data['username']))
            email = auth_form.data['username']
            password = auth_form.data['password']
            user = authenticate(username=email, password=password)
            login(request, user)
            return redirect("profile")
        else:
            logging.info("Invalid login via email/password")
            logging.debug("Email was: {}".format(auth_form.data['username']))
    else:
        # create an unbound form
        auth_form = EmailAuthenticationForm()

    return render(request, 'auth/login.html',
                  {'formset': auth_form }
    )


