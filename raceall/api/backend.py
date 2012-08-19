from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource, ALL
from raceall.models import *

from django.views.decorators.csrf import csrf_exempt
from tastypie.authorization import Authorization

class AdminUserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {
            'username': ALL,
        }

        authorization = Authorization()

class AdminRaceResource(ModelResource):
    class Meta:
        queryset = Race.objects.all()
        resource_name = 'race'
        authorization = Authorization()

class AdminRaceUsers(ModelResource):
    class Meta:
        queryset = RaceUser.objects.all()
        resource_name = 'users'
        authorization = Authorization()

#class AdminRaceTimes(ModelResource):
#    class Meta:
#        queryset = RaceTime.objects.all()
#        resource_name = 'times'
#        authorization = Authorization()

