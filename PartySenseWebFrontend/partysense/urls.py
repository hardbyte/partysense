from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from partysense.event.views import EventDetail, modify_event, get_track_list, vote_on_track
from partysense.dj.views import EventList

admin.autodiscover()

urlpatterns = patterns('',
    # enable admin
    url(r'^admin/', include(admin.site.urls)),

    # Enable the socialauth links
    url(r'', include('social_auth.urls')),

)

urlpatterns += patterns('partysense.event.views',

    # static landing page
    url(r'^$', 'landing', name='home'),

    # profile worth having (me thinks no)?
    url(r'^profile/$', 'profile'),
    url(r'^profile/logout$', 'logout'),

    url(r'^event/new/$', 'create'),

    # the actual main page
    url(r'^event/(?P<pk>\d+)/',
        ensure_csrf_cookie(EventDetail.as_view()),
        name="event-detail"),

    url(r'^api/(?P<pk>\d+)/modify',
        modify_event,
        name="modify-event"),

    url(r'^api/(?P<pk>\d+)/get-track-list',
        get_track_list,
        name="get-track-list"),

    url(r'^api/(?P<event_pk>\d+)/vote/(?P<track_pk>\d+)',
        vote_on_track,
        name="vote-on-track"),


)

urlpatterns += patterns('partysense.dj.views',
    # New dj is registering
    url(r'^register/$', 'register', name="register"),

    # List this dj's events
    url(r'^dj/(?P<dj_id>\d+)/', EventList.as_view(), name="dj_events"),
)

if settings.DEBUG:
    # serve user uploaded media
    urlpatterns += patterns('',
            (r'^media/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT}),
        )