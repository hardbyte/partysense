import json
import logging

from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import  get_object_or_404, render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings

from braces.views import LoginRequiredMixin
from partysense import fb_request
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
        dj_id = self.kwargs['dj_id']
        dj = get_object_or_404(DJ, pk=dj_id)
        queryset = dj.event_set.filter(past_event=False).order_by('-modified')
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EventList, self).get_context_data(**kwargs)
        #context['other'] = "todo"
        return context


# Form Docs https://docs.djangoproject.com/en/dev/topics/forms
# TODO replace with cbv form:
#  https://docs.djangoproject.com/en/1.5/topics/class-based-views/generic-editing/
@login_required
def register(request):
    # only show the dj registration form to user's who are not DJ's
    if DJ.objects.filter(user=request.user).exists():
        logger.info("Trying to register a second DJ for this user?")
        # TODO maybe need a DJ update view (as part of profile?)
        return HttpResponseRedirect('/event/new/')
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
            dj.user = request.user

            dj.save()

            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            # Redirect to a new event page
            return HttpResponseRedirect(reverse('event:create'))
    else:
        # Partially fill in what we know (if anything)
        # Get location from fb
        res = fb_request(request, ["location"])

        if u'error' not in res and u'location' in res:
            location = res[u'location'][u'name']
            logger.info("Facebook thinks the user is from " + location)
        else:
            location = ""

        prior_information = {
            'email': request.user.email,
            'nickname': "DJ " + request.user.first_name,
            'city_name': location
            }

        # Otherwise we are left with a completely unbound form
        form = DJForm(initial=prior_information)

    return render(
        request,
        'dj/register.html',
        {
            "formset": form,
        })


@login_required
def lookup_dj(request, q):
    """
    Given a string like "bria"
    return a list of dj instances:
    [
        {
            dj_id: 1,
            user_id: 2,
            user_name: "Brian Thorne",
            dj_name: "DJ Ango",
            city: "Christchurch, New Zealand"
        },
    ]

    """
    if len(q) < 3:
        raise Http404("Permission Denied")

    logger.info("Searching for dj for name")

    djs = []

    def add_djs_from(queryset):
        for dj in queryset:
            djs.append({
                'dj_id': dj.pk,
                'user_id': dj.user_id,
                'user_name': dj.user.get_full_name(),
                'dj_name': dj.nickname,
                'city': dj.city_name
            })

    add_djs_from(DJ.objects.filter(nickname__contains=q))
    add_djs_from(DJ.objects.filter(email__startswith=q))
    add_djs_from(DJ.objects.filter(user__first_name__startswith=q.title()))

    response = {
        'djs': djs
    }

    return HttpResponse(json.dumps(response), content_type="application/json")