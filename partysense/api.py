
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import *
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.resources import ModelResource


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']

        authorization = ReadOnlyAuthorization()
        authentication = MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())

