import json
import logging

from django.conf import settings
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.sites.models import RequestSite, Site

from registration import signals
from registration.models import RegistrationProfile
from registration.views import RegistrationView

from social.apps.django_app.default.models import UserSocialAuth
from tastypie.models import ApiKey, create_api_key

from partysense import fb_api
from partysense.psauth.forms import EmailAuthenticationForm, CustomEmailRegistrationForm

# Create a tastypie API key for any new users
models.signals.post_save.connect(create_api_key, sender=User)


class NoUserRegistrationView(RegistrationView):
    """
    A registration backend which follows a simple workflow:

    1. User signs up, inactive account is created.
    2. Email is sent to user with activation link.
    3. User clicks activation link, account is now active.
    """
    form_class = CustomEmailRegistrationForm

    SEND_ACTIVATION_EMAIL = getattr(settings, 'SEND_ACTIVATION_EMAIL', True)

    def register(self, request, **cleaned_data):
        email, password = cleaned_data['email'], cleaned_data['password1']
        site = Site.objects.get_current() if Site._meta.installed else RequestSite(request)
        username = email
        new_user = RegistrationProfile.objects.create_inactive_user(
            username, email, password, site,
            send_email=self.SEND_ACTIVATION_EMAIL,
            request=request,
        )
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def get_success_url(self, *args, **kwargs):
        return 'registration_complete', (), {}


def password_login(request):
    if request.method == 'POST':
        # Create a bound form
        auth_form = EmailAuthenticationForm(data=request.POST)
        logging.info("Authentication form valid? {}".format(auth_form.is_valid()))
        if auth_form.is_valid():
            logging.info("Email: {}".format(auth_form.data['username']))
            email = auth_form.data['username']
            password = auth_form.data['password']
            user = authenticate(username=email, password=password)

            if user is not None and not user.is_anonymous():
                login(request, user)
                return redirect("profile")
            else:
                return redirect("auth:password_login")

        else:
            logging.info("Invalid login via email/password")
            logging.debug("Email was: {}".format(auth_form.data['username']))
    else:
        # create an unbound form
        auth_form = EmailAuthenticationForm()

    return render(request, 'auth/login.html', {'formset': auth_form})


def fb_login(uid, fb_key):
    """
    Get a user from a facebook user id and access token
    """

    # Get the user's details from facebook
    res = fb_api(uid, fb_key, 'id,name')
    if 'error' in res or not res['id'] == uid:
        logging.warning("We may have been given invalid details!")
        raise HttpResponse('Unauthorized', status=401)

    name = res['name']
    logging.info("API login from {}".format(name))

    # Look for user by their fbuid in our db
    try:
        usa = UserSocialAuth.objects.get(uid=uid)
        user = usa.user
    except UserSocialAuth.DoesNotExist:
        # If user doesn't exist we need to create them
        # and link this fb account...
        logging.warning("Need to create user...")
        raise HttpResponse('Still have to do this', status=501)
    return user


def get_access_key(user):
    # See if the user has an api key, if not make one
    try:
        api_key = user.api_key
    except ApiKey.DoesNotExist:
        api_key = ApiKey.objects.create(user=user)
    return api_key.key

@csrf_exempt
@require_POST
def get_api_key(request):
    result = {"api_key": None}
    if 'email' in request.POST:
        email = request.POST["email"]
        password = request.POST['password']
        user = authenticate(username=email, password=password)
    elif 'fbuid' in request.POST:
        user = fb_login(request.POST['fbuid'], request.POST['fbkey'])
    else:
        result['status'] = "Not a valid request"
        user = None

    # return the api key and username
    result["username"] = user.username
    result["api_key"] = get_access_key(user)

    return HttpResponse(json.dumps(result), content_type="application/json")
