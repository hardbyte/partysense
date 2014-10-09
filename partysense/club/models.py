import logging
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError

from django_countries.fields import CountryField

from partysense.util.models import *
from partysense.music.models import Genre
from partysense.dj.models import DJ


class Club(models.Model):
    """
    Class to represent a Nightclub. A Nightclub needs to register for a PartySense account
    """
    # The Admin will be a number of users
    admins = models.ManyToManyField(User)

    djs = models.ManyToManyField(DJ)

    description = models.TextField(max_length=1000, verbose_name="Description", blank=True)

    # Club details
    name = models.CharField(max_length=140, verbose_name="Name of the nightclub")

    # Billing email
    email = models.EmailField(max_length=254,
                              verbose_name="Official email address for the club",
                              blank=False)

    website = models.URLField(max_length=256, verbose_name="Official Club Website", blank=True)
    facebook_page = models.URLField(max_length=256, verbose_name="Link to Facebook Page", blank=True)

    city = models.CharField(verbose_name="City", max_length=70,
                            help_text="What city is the club based in?")

    # https://bitbucket.org/smileychris/django-countries/
    country = CountryField()

    location = models.ForeignKey("event.Location", verbose_name="Where is the club?")
    
    # @TODO : Target Demographics.
    # Need a list of Tags here for the scene
    genres = models.ManyToManyField(Genre)

    # A target age group field

    cost = models.CharField(max_length=3,
                            blank=True,
                            choices=(
                                ('low', '$'),
                                ('med', '$$'),
                                ('exp', '$$$'),
                            ),
                            default='med')

    cover_charge = models.NullBooleanField(verbose_name="Cover Charge", default=False)
    live_music = models.NullBooleanField(verbose_name="Live Music")

    dress_code = models.PositiveSmallIntegerField(
        blank=True,
        choices=(
            (1, "Chilled"),
            (2, "Formal"),
            (3, "Fancy")
        ),
        default=1)

    style = models.PositiveSmallIntegerField(
        blank=True,
        choices=(
            (0, 'Chilled'),
            (1, 'Lounge'),
            (2, 'Dance Floor'),
            (3, 'Hipster'),
            (4, 'Sports Bar')
        ),
        default=0)

    uses_partysense = models.BooleanField(verbose_name="Uses Partysense", default=False)

    live_on_partysense = models.BooleanField(verbose_name="Live on Partysense", default=False)

    def __unicode__(self):
        return self.name
