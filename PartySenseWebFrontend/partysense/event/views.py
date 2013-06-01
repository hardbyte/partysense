import logging
import json
import datetime

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, UpdateView
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse

from django.conf import settings
from partysense import fb_request
from partysense.event.models import Event, Location, Vote
from partysense.dj.models import DJ
from partysense.music.models import Artist, Track, IDType

from partysense.event.forms import EventForm

import dym
logger = logging.getLogger(__name__)


class EventView():
    model = Event


class EventDetail(EventView, DetailView):

    template_name = 'event/detail.html'

    def get_object(self):
        # add this event to this user now
        return get_object_or_404(Event, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        # add other context... if required
        context['LAST_FM_API_KEY'] = settings.LASTFM_API_KEY

        # add recently up-voted tracks
        u = self.request.user
        if not u.is_anonymous():
            # TODO need to exclude ALL songs from this event, not just the upvotes from this event...
            tracks = [v.track for v in u.vote_set.all()
                                   .filter(is_positive=True)
                                   .exclude(track__in=[t.id for t in context['event'].tracks.all()])
                                   .exclude(event=context['event'])[0:10]]

            context['recent_tracks'] = tracks
        self.request.GET.next = reverse('event-detail', args=(context['event'].pk,))
        return context


@login_required
def modify_event(request, pk):
    """
    Given an event pk and a request:
        POST: New track added to event
    TODO:
        DELETE: Remove a track (TODO DJ only?)
    """
    event = get_object_or_404(Event, pk=pk)

    # First see if the user has been "added" to this event
    if not Event.objects.filter(users=request.user).exists():
        logging.info("Adding {} to event {}".format(request.user, event.title))
        event.users.add(request.user)

    data = json.loads(request.body)

    # Artist
    artist, created = Artist.objects.get_or_create(
        name=data['artist'],
        )
    if created:
        artist.spotify_url = data['spotifyArtistID']
        artist.save()

    # Track
    track, created = Track.objects.get_or_create(
        name=data['name'],
        artist=artist
        )
    if created:
        track.spotify_url = data['spotifyTrackID']

        for external_id_data in json.loads(data['external-ids']):
            id_type, created = IDType.objects.get_or_create(name=external_id_data['type'])
            track._external_ids.create(id_type=id_type, value=external_id_data['id'])

    if not event.tracks.filter(pk=track.pk).exists():
        #logger.info("Adding new track to event: {}".format(track.name))
        event.tracks.add(track)

    # Since this user added it they probably want to vote it up
    return vote_on_track(request, event.pk, track.pk, internal=True)


def get_track_list(request, pk):
    track_data = []
    event = get_object_or_404(Event, pk=pk)
    for t in event.tracks.all():
        votes = event.vote_set.filter(track=t)
        if not request.user.is_anonymous() and votes.filter(user=request.user).exists():
            usersVote = votes.get(user=request.user).is_positive
        else:
            usersVote = None
        track_data.append({
            'pk': t.pk,
            "name": t.name,
            "artist": t.artist.name,
            "spotifyTrackID": t.spotify_url,
            "spotifyArtistID": t.artist.spotify_url,
            "external-ids": t.external_ids,
            "upVotes": votes.filter(is_positive=True).count(),
            "downVotes": votes.filter(is_positive=False).count(),
            "usersVote": usersVote
        })

    return HttpResponse(json.dumps(track_data), content_type="application/json")

@login_required
def did_you_mean(request):
    logging.info("Checking spelling")
    q = request.GET["q"]
    return HttpResponse(json.dumps({'changed': dym.didYouMean(q)}),
                        content_type="application/json")

@login_required
def vote_on_track(request, event_pk, track_pk, internal=False):
    event = get_object_or_404(Event, pk=event_pk)

    if not event.users.filter(pk=request.user.pk).exists():
        event.users.add(request.user)

    # Check that this user hasn't voted on this event and track
    logger.info("User: {} is voting on track:{}".format(request.user.first_name, track_pk))
    vote, created = Vote.objects.get_or_create(
        event=event,
        user=request.user,
        track_id=track_pk
    )
    if internal:
        voteDirection = True
    else:
        data = json.loads(request.body)
        voteDirection = data['vote']
    vote.is_positive = voteDirection
    vote.save()
    return HttpResponse(json.dumps({'created': created}), content_type="application/json")


# Form Docs https://docs.djangoproject.com/en/dev/topics/forms
# TODO replace with cbv CreateView:
#  https://docs.djangoproject.com/en/1.5/topics/class-based-views/generic-editing/
@login_required
def create(request):
    # If user hasn't yet registered as a dj get them to do that first...
    if not DJ.objects.filter(user=request.user).exists():
        return HttpResponseRedirect('/register/')

    if request.method == 'POST':
        # If the form has been submitted...
        # A form bound to the POST data
        event_form = EventForm(request.POST)

        if event_form.is_valid():
            # All validation rules pass
            # Process the data in form.cleaned_data and create an
            # instance out of it:
            event = event_form.save(commit=False)
            logger.info("Creating new event to start at: {}".format(event.start_time))
            # Add the automatic fields based on user
            # assumes the user is already a DJ
            event.dj = DJ.objects.get(user=request.user.id)

            # create a new location or use existing...
            location = Location(
                name=event_form.cleaned_data['venue'],
                latitude=event_form.cleaned_data['latitude'],
                longitude=event_form.cleaned_data['longitude'],
            )
            location.save()
            event.location = location

            # todo get fb event url from incoming link?
            event.fb_url = "http://facebook.com/event"

            # then commit the new event to our database
            event.save()

            # TODO Redirect using reverse lookup...
            return HttpResponseRedirect('/event/{}/{}'.format(event.pk, event.slug))
    else:
        # Partially fill in what we know (if anything)
        now = datetime.datetime.now()
        if now.weekday < 6:
            saturday = now + datetime.timedelta(days=(5 - now.weekday()))
        else:
            # its sunday
            saturday = now + datetime.timedelta(days=6)
        next_saturday = datetime.datetime(year=saturday.year, month=saturday.month, day=saturday.day, hour=19)

        prior_information = {'start_time': next_saturday}
        # Otherwise we are left with a completely unbound form
        event_form = EventForm(initial=prior_information)

    return render(request,
                  'event/new.html',
                  {
                      "formset": event_form
                  })


def profile(request):
    if request.user.is_authenticated() and 'next' in request.GET:
        #return HttpResponseRedirect('done')
        logging.info("Maybe should be redireting now? " + request.GET['next'])

    img = None
    past_events = []
    upcoming_events = []

    if request.user.is_authenticated():
        res = fb_request(request, "picture.width(200).type(square)")
        if 'error' not in res and 'picture' in res:
            img = res['picture']['data']

        # Get past_events
        past_events = Event.objects.filter(users=request.user, past_event=True)

        # Upcoming events
        upcoming_events = Event.objects.filter(users=request.user, past_event=False)

    # TODO: Also show events by dj's this user has attended events of in the past

    djs = DJ.objects.filter(event__past_event=False).distinct()

    """See what we can get from facebook
    Some users have "music", some who use spotify have "music.listens" and "music.playlists"
    Many (such as myself) have nothing available.

    listens have data.song.title
    """
    listens = fb_request(request, ["music.listens"])["music.listens"]['data']

    return render(request, 'profiles/detail.html', {
        "img": img,
        "djs": djs,
        "past_events": past_events,
        "listens": listens,
        "upcoming_events": upcoming_events
    })


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')


def landing(request):
    # List upcoming "public" events
    return render(request, 'landing.html', {})

def privacy(request):
    return render(request, 'privacy.html')

@permission_required("can_change_past_event")
def mark_over(request, pk):
    event = Event.objects.get(pk=pk)
    event.past_event = True
    event.save()
    return HttpResponseRedirect(reverse("admin:todo_changelist"))