import logging

from django.shortcuts import get_object_or_404, render, redirect

from django.core.urlresolvers import reverse
from django.views.generic import DetailView

from django.contrib.auth.decorators import login_required


from partysense.club.models import Club
from partysense.event.models import Location

from partysense.club.forms import NewClubForm


def landing(request):
    return render(request, 'club/landing.html')


class ClubDetail(DetailView):
    model = Club
    template_name = 'club/detail.html'


@login_required
def create_club(request):
    """
    Create a new Club
    """
    if request.method == "POST":
        club_form = NewClubForm(data=request.POST)
        if club_form.is_valid():

            club_email = club_form.cleaned_data['email']
            club_name = club_form.cleaned_data['name']

            logging.info("Registering new club {} with contact email <{}>".format(club_name, club_email))
            new_club = club_form.save(commit=False)
            logging.info("Created a new club: {}".format(new_club.name))

            # create a new location or use existing...
            location = Location(
                name=club_name,
                latitude=0.0, #club_form.cleaned_data['latitude'],
                longitude=0.0 #club_form.cleaned_data['longitude'],
            )
            location.save()
            new_club.location = location
            new_club.save()

            # After the club has been added (and has an identifier) we can use many to many relationships
            new_club.admins.add(request.user)


            return redirect(reverse("club-profile", args=(new_club.pk,)))
    else:
        # Use logged in users email (if we have it)
        club_form = NewClubForm(initial={
            'email': request.user.email,
        })

    return render(request,
                  'club/register.html',
                  { 'formset' : club_form })