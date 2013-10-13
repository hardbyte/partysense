__author__ = 'Brian'

import logging
from django.db import models
from django.core.cache import cache


"""
To keep our options for shifting backends open I'll allow multiple
external ID's.

For reference spotify gives something like this:
    artists: [{href:spotify:artist:08F3Y3SctIlsOEmKd6dnH8, name:Cat Stevens}]
    external-ids: [{type:isrc, id:GBAAN7000041}]
    href: "spotify:track:5dEIKV9qPHxXyLL79m9UBD"

Last.fm gives:
    artist: {name:Cat Stevens, mbid:5adb8b74-54b8-4700-836e-550b6a2a2f71, url:http://www.last.fm/music/Cat+Stevens}
    id: "1003366"
    listeners: "400028"
    mbid: "7d7e146d-0742-4236-a880-926f38581750"
"""


class IDType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class ExternalID(models.Model):
    id_type = models.ForeignKey('IDType')
    value = models.CharField(max_length=64)

    def __repr__(self):
        return '<{s.id_type.name}: "{s.value}">'.format(s=self)


class ExternallyDefinedIDModel(models.Model):
    _spotify_type = IDType.objects.get(pk=1)
    _external_ids = models.ManyToManyField(ExternalID)

    def get_spotify_url(self):
        # Look up the external ids and find the "spotify" one
        cache_key = "spotifyid:{}:{}".format(self.__class__.__name__, self.pk)
        spotify_id = cache.get(cache_key)
        if spotify_id is None:
            spotify_id = self._external_ids.only("value").get(id_type=self._spotify_type).value
            cache.set(cache_key, spotify_id, 9999)
        return spotify_id


    def set_spotify_url(self, value):
        self._external_ids.create(id_type=self._spotify_type, value=value)

    spotify_url = property(get_spotify_url, set_spotify_url)

    @property
    def external_ids(self):
        # Create a {"spotify": "spotify:url:4y5fy", ...} dict
        res = {}
        for eid in self._external_ids.all():
            res[eid.id_type.name] = eid.value
        return res

    class Meta:
        abstract = True


class Artist(ExternallyDefinedIDModel):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

    def track_count(self):
        return self.tracks().count()

    def tracks(self):
        """Get all tracks by this artist"""
        return Track.objects.filter(artist=self.pk)


class Track(ExternallyDefinedIDModel):
    artist = models.ForeignKey('Artist')
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.artist.name + ": " + self.name
