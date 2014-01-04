# Tastypie API Resources
from tastypie import fields
from tastypie.resources import ModelResource, ALL
from partysense.club.models import Club
from partysense.api import UserResource
from partysense.util.api import LocationResource

# TODO http://django-tastypie.readthedocs.org/en/latest/geodjango.html


class ClubResource(ModelResource):

    admins = fields.ToManyField(UserResource, 'admins')
    location = fields.ToOneField(LocationResource, 'location', full=True)

    class Meta:
        queryset = Club.objects.all()
        resource_name = 'club'
        filtering = {
            'country': ALL,
            'city': ALL
        }
