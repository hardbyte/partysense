import logging
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db.models.signals import post_save

from partysense.dj.models import DJ


logger = logging.getLogger(__name__)
logger.debug("Parsing models.py")


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self updating
    ``created`` and ``modified`` fields.

    Taken from Two Scoops of Django
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created']


class Location(models.Model):
    """
    """

    # Club/Bar/Venue name
    name = models.CharField(max_length=50, blank=True, help_text="Venue")

    # Address as entered
    address = models.CharField(max_length=92 )

    # coordinate as returned by google maps
    coordinate = models.CharField(max_length=64, editable=False)

    def __unicode__(self):
        return unicode(self.name)


class Event(TimeStampedModel):
    """
    The core of the system
    """
    title = models.CharField("Event name", max_length=70)
    location = models.ForeignKey(Location, help_text="Where is the event?")
    dj = models.ForeignKey(DJ, editable=False)

    # date & time info
    # note we also have a "created" and "modified" attribute
    past_event = models.BooleanField(default=False, editable=False)
    happening_now = models.BooleanField(default=False)

    start_time = models.DateTimeField()

    fb_url = models.URLField(editable=False)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.title)


    #def tracks(self):
    #    return Track.objects.filter(events_set=self).count()

