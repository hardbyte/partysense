import logging
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db.models.signals import post_save

from partysense.dj.models import DJ
from partysense.music.models import Track, Artist

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
    address = models.CharField(max_length=92, blank=True)

    # coordinate as returned by google maps
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return unicode(self.name)


class Event(TimeStampedModel):
    """
    The core of the system
    """
    title = models.CharField("Event name", max_length=70, help_text="Keep it simple")
    location = models.ForeignKey(Location, help_text="Where is the event?")
    dj = models.ForeignKey(DJ)
    users = models.ManyToManyField(User, blank=True)
    tracks = models.ManyToManyField(Track, blank=True)

    # date & time info
    # note we also have a "created" and "modified" attribute
    past_event = models.BooleanField(default=False, editable=False)

    # The DJ can choose all the music or users can add too
    user_editable = models.BooleanField(default=True,
                                        verbose_name="Anyone can add new music?",
                                        help_text="Otherwise you add the music, and everyone else votes.")

    start_time = models.DateTimeField()

    fb_url = models.URLField(editable=False)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.title)

    def __str__(self):
        return str(self.title)

class Vote(models.Model):
    event = models.ForeignKey(Event, db_index=True)
    user = models.ForeignKey(User, db_index=True)
    track = models.ForeignKey(Track, db_index=True)
    is_positive = models.BooleanField()

    def __str__(self):
        return self.user.first_name + ": " + self.track.name