import logging

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django import forms

from partysense.club.models import Club


class UserCreateForm(UserCreationForm):
    club_name = forms.CharField(label="Club Name", required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "club_name")


def landing(request):
    return render(request, 'club/landing.html', {'formset': AuthenticationForm(request.POST)})


class ClubDetail(DetailView):
    model = Club
    template_name = 'club/detail.html'


def create_club(request):
    """
    Create a new Club
    """
    user_form = UserCreateForm(request.POST)
    if user_form.is_valid():
        username = user_form.clean_email()
        password = user_form.clean_password2()
        club_name = user_form.clean_club_name()
        logging.info("Registering new club {}".format(club_name))
        user_form.save()
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(reverse("club-profile"))
    return render(request,
                  'club/register.html',
                  { 'formset' : user_form })