import logging
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.timezone import utc
from django.core.urlresolvers import reverse

from partysense.dj.models import DJ
from partysense.music.models import Track
from partysense.util.models import *

logger = logging.getLogger(__name__)
logger.debug("Parsing models.py")


class Location(models.Model):
    """
    Keeps track of an event/club location.

    TODO: migrate into the util app
    """

    # Club/Bar/Venue name
    name = models.CharField(max_length=256, blank=True, help_text="Venue")

    # coordinate as returned by google maps
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return unicode(self.name)


class Event(TimeStampedModel):
    """
    The core of the system
    """
    title = models.CharField("Event Name", max_length=70, help_text="Keep it simple")

    description = models.TextField("Event Description", blank=True,
                                   help_text="""Guidance to attendees about what to expect.
    <strong>Eg:</strong>
    <blockquote>We will play any tracks with more than 10 up votes</blockquote>

    """)

    location = models.ForeignKey(Location, help_text="Where is the event?")

    # TODO migrate to multiple dj's
    dj = models.ForeignKey(DJ)
    users = models.ManyToManyField(User, blank=True)
    tracks = models.ManyToManyField(Track, blank=True)

    # date & time info
    # note we also have a "created" and "modified" attribute
    past_event = models.BooleanField(default=False, editable=False)

    # The DJ can choose all the music or users can add too
    user_editable = models.BooleanField(default=True,
                                        verbose_name="Allow guests to add music to the playlist (Recommended) ",
                                        help_text="""If not selected, only Event DJs can add songs to the playlist.
                                        Other users will still be able to vote on the music you have chosen.""")

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

    def timedelta(self):
        return self.start_time - datetime.datetime.utcnow().replace(tzinfo=utc)

    def get_absolute_url(self):
        return reverse('event:detail', args=[str(self.id), self.slug])


class Vote(models.Model):
    event = models.ForeignKey(Event, db_index=True)
    user = models.ForeignKey(User, db_index=True)
    track = models.ForeignKey(Track, db_index=True)
    is_positive = models.BooleanField()

    def __str__(self):
        return self.user.first_name + ": " + self.track.name