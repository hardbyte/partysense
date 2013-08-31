from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from registration.backends.default.views import RegistrationView

from partysense.event.views import *
from partysense.club.views import *
from partysense.dj.views import EventList
from partysense.auth.views import *

from partysense.auth.forms import CustomEmailRegistrationForm
admin.autodiscover()

urlpatterns = patterns('',
    # enable admin
    url(r'^admin/', include(admin.site.urls)),

    # Enable the socialauth links
    url(r'', include('social_auth.urls')),

    # add a page that allows users to login with a password
    url(r'^accounts/login/', password_login, name='password_login'),

    # Registration links
    url(r'^accounts/', include('registration_email.backends.default.urls')),
    url(r'^accounts/register/$',
        RegistrationView.as_view(
            template_name='registration/registration_form.html',
            form_class=CustomEmailRegistrationForm,
            success_url=getattr(
                settings, 'REGISTRATION_EMAIL_REGISTER_SUCCESS_URL', None),
        ),
        name='registration_register',
    ),


    # add a page that purposely errors to test logging etc
    url(r'^500$', 'unknown'),


)

urlpatterns += patterns('partysense.event.views',

    # static landing page
    url(r'^$', 'landing', name='home'),

    url(r'^privacy/$', 'privacy', name='privacy'),

    # profile worth having (me thinks no)?
    url(r'^profile/$', 'profile', name="profile"),
    url(r'^profile/logout/$', 'logout', name='logout'),

    url(r'^event/new/$', 'create', name="create-event"),

    # the actual main event page
    url(r'^event/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        ensure_csrf_cookie(EventDetail.as_view()),
        name="event-detail"),

    # statistics page
    url(r'^event/(?P<pk>\d+)/(?P<slug>[-\w]+)/stats/$',
        login_required(EventStatsDetail.as_view()),
        name="event-stats"),

    # edit view
    url(r'^event/(?P<pk>\d+)/(?P<slug>[-\w]+)/edit/$',
        'update',
        name="event-update"),
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
    # serve user uploaded media
    urlpatterns += patterns('',
            (r'^media/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT}),
        )
