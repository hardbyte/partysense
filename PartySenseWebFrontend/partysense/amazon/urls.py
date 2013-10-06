from django.conf.urls import patterns, url
from django.views.decorators.csrf import ensure_csrf_cookie

from partysense.amazon.views import *

urlpatterns = patterns('',
    # add an api call for searching amazon for a mp3 product
    url(r'^purchase/$', purchase, name='purchase'),

    )