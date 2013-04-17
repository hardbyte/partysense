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

from partysense.event.models import Event
#from partysense.music import Track, Artist

from models import DJ
from forms import DJForm

logger = logging.getLogger(__name__)


class EventList(ListView):
    model = Event

    # Note django defaults to using template of "list.html"
    template_name = 'event/list.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        logger.debug("filter out finished events and events that aren't visible to this dj/user")
        queryset = Event.objects.filter(past=False)

        # TODO just get this dj's events

        return queryset.order_by('-date_created')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EventList, self).get_context_data(**kwargs)

        context['other'] = "todo"

        return context


# Form Docs https://docs.djangoproject.com/en/dev/topics/forms
# TODO replace cbv form:
#  https://docs.djangoproject.com/en/1.5/topics/class-based-views/generic-editing/
@login_required
def register(request):

    if request.method == 'POST':
        # If the form has been submitted...
        # A form bound to the POST data
        form = DJForm(request.POST)
        if form.is_valid():
            # All validation rules pass
            # Process the data in form.cleaned_data

            # Now we make an instance out of the data
            dj = form.save(commit=False)

            # Add the automatic fields based on user's preferences
            dj.user = request.user.id

            dj.save()

            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            # Redirect to a thanks for joining page
            return HttpResponseRedirect('/event/new')
    else:
        # Partially fill in what we know (if anything)
        prior_information = {}

        # Otherwise we are left with a completely unbound form
        form = DJForm(initial=prior_information)

    return render(request,
                  'dj/register.html',
                  {
                      "formset": form,
                  })
