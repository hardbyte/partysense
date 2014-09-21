from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api

from partysense.event.urls import *
from partysense.club.views import *
from partysense.dj.views import EventList, lookup_dj

from partysense.club.api import ClubResource
from partysense.api import UserResource
from partysense.util.api import LocationResource


admin.autodiscover()

urlpatterns = patterns('',
    # enable admin
    url(r'^admin/', include(admin.site.urls)),

    url(r'^bigbrother/', include('bigbrother.urls')),

    url(r'^event/', include('partysense.event.urls', namespace="event")),

    url(r'^club/', include('partysense.club.urls', namespace='club')),

    # Enable the socialauth links
    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^amazon/', include('partysense.amazon.urls', namespace="amazon")),

    url(r'^accounts/', include('partysense.auth.urls', namespace="auth")),

    # Registration links
    url(r'^accounts/', include('registration_email.backends.default.urls')),

    # add a page that purposely errors to test logging etc
    url(r'^500$', 'unknown'),


)

v1_api = Api(api_name='v1')
#v1_api.register(UserResource())
v1_api.register(ClubResource())
v1_api.register(LocationResource())

urlpatterns += patterns('partysense.event.views',

    # static landing page
    url(r'^$', 'landing', name='home'),

    url(r'^privacy/$', 'privacy', name='privacy'),

    # profile worth having (me thinks no)?
    url(r'^profile/$', 'profile', name="profile"),

    # These next urls form the javascript API

    url(r'^api/', include(v1_api.urls)),

    url(r'^api/(?P<pk>\d+)/modify',
        modify_event,
        name="modify-event"),

    url(r'^api/(?P<pk>\d+)/get-track-list',
        get_track_list,
        name="get-track-list"),

    url(r'^api/(?P<event_pk>\d+)/vote/(?P<track_pk>\d+)',
        vote_on_track,
        name="vote-on-track"),

    url(r'^api/(?P<event_pk>\d+)/remove/(?P<track_pk>\d+)',
        remove_track,
        name="remove-track"),

    url(r'^did-you-mean',
        did_you_mean,
        name="did-you-mean"),

)

urlpatterns += patterns('partysense.dj.views',
    # New dj is registering
    url(r'^dj/register/$', 'register', name="register"),

    # List this dj's events
    url(r'^dj/(?P<dj_id>\d+)/', EventList.as_view(), name="dj_events"),

    # Search for a dj
    url(r'^dj/search/(?P<q>\w+)/', lookup_dj, name="dj_search"),
)



if settings.DEBUG:
    # During development django can serve media and static files.

    urlpatterns += patterns('',
            (r'^media/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT}),
        )

    urlpatterns += patterns('',
            (r'^static/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': settings.STATIC_ROOT}),
        )
