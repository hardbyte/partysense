from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ( "email", )


def landing(request):
    return render(request, 'club/clubs.html')


def create_club(request):
    """
    Create a new Club
    """
    user_form = UserCreateForm(request.POST)
    if user_form.is_valid():
        username = user_form.clean_username()
        password = user_form.clean_password2()
        user_form.save()
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("somewhere")
    return render(request, 'club/register.html',
                  { 'formset' : user_form })