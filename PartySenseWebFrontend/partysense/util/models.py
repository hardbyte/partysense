import logging

from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self updating
    ``created`` and ``modified`` fields.

    Taken from Two Scoops of Django
    TODO: django-model-utils could provide this
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created']

