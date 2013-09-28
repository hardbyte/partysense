from django.conf.urls import patterns, url
from django.views.decorators.csrf import ensure_csrf_cookie

from event.views import *

urlpatterns = patterns('',

    url(r'^new/$', 'create', name="create"),

    # the actual main event page
    url(r'^(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        ensure_csrf_cookie(EventDetail.as_view()),
        name="detail"),

    # statistics page
    url(r'^(?P<pk>\d+)/(?P<slug>[-\w]+)/stats/$',
        login_required(EventStatsDetail.as_view()),
        name="stats"),

    # edit view
    url(r'^(?P<pk>\d+)/(?P<slug>[-\w]+)/edit/$',
        'update',
        name="update")
)