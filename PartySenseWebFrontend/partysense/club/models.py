import logging
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError

from django_countries import CountryField

from partysense.util.models import *


class Club(models.Model):
    """
    Class to represent a Nightclub. A Nightclub needs to register for a PartySense account
    """
    # The Admin will be a number of users
    admins = models.ManyToManyField(User)

    description = models.TextField(max_length=1000, verbose_name="Description")

    # Club details
    name = models.CharField(max_length=140, verbose_name="Name of the nightclub")

    # Billing email
    email = models.EmailField(max_length=254,
                              verbose_name="Official email address for the club",
                              blank=False)

    website = models.URLField(max_length=70, verbose_name="Official Club Website", blank=True)
    facebook_page = models.URLField(max_length=70, verbose_name="Link to Facebook Page", blank=True)

    city = models.CharField(verbose_name="City", max_length=70,
                            help_text="What city are you based in?")

    # https://bitbucket.org/smileychris/django-countries/
    country = CountryField()

    location = models.ForeignKey("event.Location", verbose_name="Where is the club?")
    
    # @TODO : Genres and Demographics. 
    # Need a list of Tags here for music genres and the scene
    # Also need an age group field


    def __str__(self):
        return self.name
