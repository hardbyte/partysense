import logging
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError


class Club(models.Model):
    """
    Class to represent a Nightclub. A Nightclub needs to register for a PartySense account
    """

	# The Admin will be a user. Down the line we can allow multiple administrators for a fee
    admin_user = models.ForeignKey(User) 
	description = models.TextField(max_length=1000, verbose_name="Description")
	
	
    # Club details. A part of this should be extracted out into a separate model for a Place ?
    club_name = models.CharField(max_length=140, verbose_name="Name of the nightclub")
    club_id = models.CharField(maxLength=70) #  Automatically generated Unique ID for the club based on name and city? 
    club_email = models.EmailField(max_length=254, verbose_name="Official Email address for the club")
    website = models.URLField(max_length=70, verbose_name="Official Club Website")
    facebook_page = models.URLField(max_length=70, verbose_name="Link to Facebook Page")
    address = models.CharField(max_length=92, blank=True)
    city = models.CharField(verbose_name="Location", max_length=70,
                                 help_text="What city are you based in?")
    country = models.CharField(verbose_name="Location", max_length=70,
                                 help_text="What city are you based in?")
    latitude = models.FloatField() # Internal Use. Coordinates from Google Maps
    longitude = models.FloatField() # Internal Use. Coordinates from Google Maps
    
    # @TODO : Genres and Demographics. 
    # Need a list of Tags here for music genres and the scene
    # Also need an agegroup field


    def __str__(self):
        return self.club_id
