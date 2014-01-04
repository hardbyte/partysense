from tastypie import fields
from tastypie.resources import ModelResource
from partysense.event.models import Location

class LocationResource(ModelResource):
    class Meta:
        queryset = Location.objects.all()
        resource_name = 'location'
