import logging
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError

class DJ(models.Model):
    """
    Any fb user can become a `DJ` by registering their details.
    """

    user = models.ForeignKey(User)
    nickname = models.CharField(max_length=70, verbose_name="Alias")
    # Contact details
    email = models.EmailField(max_length=254,)

    # Business details ?
    # A DJ might be associated with a business/club? ... do we care?
    # TODO: maybe should be mandatory?
    #business = models.ForeignKey("Club", blank=True)

    # DJ will probably have a profile on facebook?
    url = models.URLField(verbose_name="Facebook Page or website", blank=True)

    #picture =

    city_name = models.CharField(verbose_name="Location", max_length=70,
                                 help_text="What city are you based in?")

    def __str__(self):
        return self.nickname