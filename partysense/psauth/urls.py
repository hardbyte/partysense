from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

from partysense.psauth.forms import CustomEmailRegistrationForm
from partysense.psauth.views import *

urlpatterns = patterns('',


    # add a custom page that allows users to login with a password or oauth
    url(r'^login/$', password_login, name='password_login'),

    url(r'^api-login/$', get_api_key, name='api_login'),

    url(
        r'^logout/$',
        auth_views.logout,
        {'next_page': '/'},
        name='password_logout',
    ),

    # page that allows registration of new users with an email + password
    url(r'^register/$',
        NoUserRegistrationView.as_view(),
        name='registration_register',
    )
)