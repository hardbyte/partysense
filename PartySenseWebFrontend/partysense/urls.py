from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


from partysense.event.urls import *

from partysense.club.views import *
from partysense.dj.views import EventList



admin.autodiscover()

urlpatterns = patterns('',
    # enable admin
    url(r'^admin/', include(admin.site.urls)),

    url(r'^event/', include('partysense.event.urls', namespace="event")),

    # Enable the socialauth links
    url('', include('social.apps.django_app.urls', namespace='social')),


    url(r'^accounts/', include('partysense.auth.urls', namespace="auth")),
    # Registration links
    url(r'^accounts/', include('registration_email.backends.default.urls')),

    # add a page that purposely errors to test logging etc
    url(r'^500$', 'unknown'),


)

urlpatterns += patterns('partysense.event.views',

    # static landing page
    url(r'^$', 'landing', name='home'),

    url(r'^privacy/$', 'privacy', name='privacy'),

    # profile worth having (me thinks no)?
    url(r'^profile/$', 'profile', name="profile"),

    # These next urls form the javascript API

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
)

urlpatterns += patterns('partysense.club.views',
    url(r'^club/$', 'landing', name='club-landing'),
    url(r'^club/new/$', 'create_club', name='create-club'),
    url(r'^club/(?P<pk>\d+)/', ClubDetail.as_view(), name='club-profile'),
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
