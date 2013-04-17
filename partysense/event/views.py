import logging
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.shortcuts import  get_object_or_404, render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings

from braces.views import LoginRequiredMixin

from partysense.event.models import Event, Location
from partysense.dj.models import DJ

from partysense.event.forms import EventForm

logger = logging.getLogger(__name__)


class EventDetail(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'event/detail.html'
    context_object_name = 'event'
    pk_url_kwarg = 'event_id'

    def get_object(self):
        # TODO add view count here ?
        return get_object_or_404(Event, pk=self.kwargs['event_id'])

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        # add other context... if required
        return context


# Form Docs https://docs.djangoproject.com/en/dev/topics/forms
# TODO replace cbv form:
#  https://docs.djangoproject.com/en/1.5/topics/class-based-views/generic-editing/
#@login_required
def create(request):
    if request.method == 'POST':
        # If the form has been submitted...
        # A form bound to the POST data
        form = EventForm(request.POST)
        if form.is_valid():
            # All validation rules pass
            # Process the data in form.cleaned_data and create an
            # instance out of it:
            event = form.save(commit=False)
            logger.info("Creating new event to start at: {}".format(event.start_time))
            # Add the automatic fields based on user
            event.dj = DJ.object.get(user=request.user.id)

            # TODO create a new location or use existing...
            location = Location(name="The Bush", address="Bush Inn, Christchurch")
            location.save()
            event.location = location

            # todo get fb event url from incoming link?
            event.fb_url = "http://facebook.com/event"

            # then commit the new event to our database
            event.save()

            # TODO Redirect to something in particular?
            return HttpResponseRedirect('/')
    else:
        # Partially fill in what we know (if anything)
        prior_information = {}


        # Otherwise we are left with a completely unbound form
        formset = EventForm(initial=prior_information)

        return render(request,
                      'event/new.html',
                      {
                          "formset": formset,

                      })


def profile(request):
    if request.user.is_authenticated() and 'next' in request.GET:
        #return HttpResponseRedirect('done')
        logging.info("Maybe should be redireting now? " + request.GET['next'])
    return render(request, 'profiles/detail.html')


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')


def landing(request):
    return render(request, 'landing.html',
        {
            'djs': DJ.objects.all(),
        })


@permission_required("can_change_past_event")
def mark_over(request, pk):
    event = Event.objects.get(pk=pk)
    event.past_event = True
    event.save()
    return HttpResponseRedirect(reverse("admin:todo_changelist"))