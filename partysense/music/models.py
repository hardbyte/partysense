__author__ = 'Brian'

import logging
from django.db import models


class SpotifyBackedModel(models.Model):
    # Something like "spotify:artist:7jy3rLJdDQY21OgRLCZ9sD"
    spotify_url = models.CharField(max_length=80, unique=True)

    class Meta:
        abstract = True


class Artist(SpotifyBackedModel):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    def track_count(self):
        return self.tracks().count()

    def tracks(self):
        """Get all tracks by this artist"""
        return Track.objects.filter(artist=self.pk)


class Track(SpotifyBackedModel):
    artist = models.ForeignKey('Artist')
    name = models.CharField(max_length=80)

    # Out of spotify api: [{type:isrc, id:USRW30500001}]
    external_ids = models.CharField(max_length=512, blank=True)

    def __repr__(self):
        return self.artist.name + ": " + self.name
