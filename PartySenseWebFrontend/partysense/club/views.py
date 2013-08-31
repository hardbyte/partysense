import logging

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django import forms

from partysense.event.models import Location
from partysense.club.models import Club


class NewClubForm(forms.ModelForm):

    class Meta:
        model = Club
        fields = ("name", "email", "website", "facebook_page", "city", "country",)


def landing(request):
    return render(request, 'club/landing.html')


class ClubDetail(DetailView):
    model = Club
    template_name = 'club/detail.html'


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


            return redirect(reverse("club-profile", new_club.pk))
    else:
        # Use logged in users email (if we have it)
        club_form = NewClubForm(initial={
            'email': request.user.email,
        })

    return render(request,
                  'club/register.html',
                  { 'formset' : club_form })