from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import permission_required, login_required

from partysense.event.views import EventDetail
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

    # the actual main page
    url(r'^event/(?P<event_id>\d+)/', EventDetail.as_view(), name="event"),

    url(r'^event/new$', 'create'),
)

urlpatterns += patterns('partysense.dj.views',
    # New dj is registering
    url(r'^register/$', 'register', name="register"),

    # List this dj's events
    # TODO add permission required decorator
    url(r'^dj/(?P<event_id>\d+)/', EventList.as_view(), name="dj_events"),
)


if settings.DEBUG:
    # serve user uploaded media
    urlpatterns += patterns('',
            (r'^media/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT}),
        )