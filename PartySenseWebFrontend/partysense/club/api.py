# Tastypie API Resources
from tastypie import fields
from tastypie.resources import ModelResource
from partysense.club.models import Club
from partysense.api import UserResource
from partysense.util.api import LocationResource

class ClubResource(ModelResource):

    admins = fields.ToManyField(UserResource, 'admins')
    location = fields.ForeignKey(LocationResource, 'location')

    class Meta:
        queryset = Club.objects.all()
        resource_name = 'club'
