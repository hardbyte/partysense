from django.conf import settings
from django.conf.urls import patterns, url

from registration.backends.default.views import RegistrationView

from auth.forms import CustomEmailRegistrationForm
from auth.views import *

urlpatterns = patterns('',


    # add a custom page that allows users to login with a password or oauth
    url(r'^login/$', password_login, name='password_login'),

    # page that allows registration of new users with an email + password
    url(r'^register/$',
        RegistrationView.as_view(
            template_name='registration/registration_form.html',
            form_class=CustomEmailRegistrationForm,
            success_url=getattr(
                settings, 'REGISTRATION_EMAIL_REGISTER_SUCCESS_URL', None),
        ),
        name='registration_register',
    )
)