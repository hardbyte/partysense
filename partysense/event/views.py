import logging
import json
import datetime

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, UpdateView
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse


from braces.views import LoginRequiredMixin

from django.conf import settings
from partysense import fb_request
from partysense.event.models import Event, Location, Vote
from partysense.dj.models import DJ
from partysense.music.models import Artist, Track

from partysense.event.forms import EventForm

logger = logging.getLogger(__name__)

class EventView(LoginRequiredMixin):
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
        return context


@login_required
def modify_event(request, pk):
    """
    Given an event pk and a request:
        POST: New track added to event
    TODO the rest:
        PUT/PATCH: Change the rank of an existing track
        DELETE: Remove a track (TODO DJ only?)
    """
    event = get_object_or_404(Event, pk=pk)

    # First see if the user has been "added" to this event
    if not Event.objects.filter(users=request.user).exists():
        logging.info("Adding {} to event {}".format(request.user, event.title))
        event.users.add(request.user)

    data = json.loads(request.body)
    #data = request.POST
    # Artist
    artist, created = Artist.objects.get_or_create(
        name=data['artist'],
        spotify_url=data['spotifyArtistID']
        )

    # Track
    track, created = Track.objects.get_or_create(
        name=data['name'],
        artist=artist,
        spotify_url=data['spotifyTrackID'],
        external_ids=json.loads(data['external-ids']),
        )

    if not event.tracks.filter(pk=track.pk).exists():
        logger.info("Adding new track to event: {}".format(track.name))
        event.tracks.add(track)

    # Since this user added it they probably want to vote it up
    return vote_on_track(request, event.pk, track.pk, internal=True)


def get_track_list(request, pk):
    track_data = []
    event = get_object_or_404(Event, pk=pk)
    for t in event.tracks.all():
        votes = event.vote_set.filter(track=t)
        if votes.filter(user=request.user).exists():
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
    response_data = {"tracks": track_data}

    return HttpResponse(json.dumps(response_data), content_type="application/json")

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
        track_id=track_pk,
    )
    vote.is_positive = internal or request.POST['vote'] == u"true"
    vote.save()
    return HttpResponse(json.dumps({'created': created}), content_type="application/json")


# Form Docs https://docs.djangoproject.com/en/dev/topics/forms
# TODO replace with cbv CreateView:
#  https://docs.djangoproject.com/en/1.5/topics/class-based-views/generic-editing/
@login_required
def create(request):
    # If user hasn't yet registered as a dj get them to do that first...
    if not DJ.objects.filter(user=request.user).exists():
        return HttpResponseRedirect('/register')

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
        saturday = now + datetime.timedelta(days=(5 - now.weekday()))
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
    if request.user.is_authenticated():
        res = fb_request(request, "picture.width(200).type(square)")
        if 'error' not in res and 'picture' in res:
            img = res['picture']['data']
    return render(request, 'profiles/detail.html', {
        "img": img
    })


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')


def landing(request):
    # List upcoming "public" events
    djs = DJ.objects.filter(event__past_event=False)
    return render(request, 'landing.html',
        {
            'djs': djs,
        })


@permission_required("can_change_past_event")
def mark_over(request, pk):
    event = Event.objects.get(pk=pk)
    event.past_event = True
    event.save()
    return HttpResponseRedirect(reverse("admin:todo_changelist"))