from django.conf.urls import patterns, url, include
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.cache import cache_page
from partysense.club.views import *

urlpatterns = patterns('',
    url(r'^$', landing, name='landing'),
    url(r'^new/$', create_club, name='create'),
    url(r'^(?P<pk>\d+)/', ClubDetail.as_view(), name='profile'),
)