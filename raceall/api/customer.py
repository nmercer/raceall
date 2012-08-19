from django.contrib.auth.models import User
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL
from raceall.models import *
from django.views.decorators.csrf import csrf_exempt
from tastypie.authorization import Authorization
from auth import *
import json


class FriendshipResource(ModelResource):
    users = fields.ToOneField('raceall.api.backend.AdminUserResource', 'user', full=True)

    class Meta:
        queryset = Friendship.objects.all()
        resource_name = 'friends'
        allowed_methods = ['get', 'post', 'delete']

        authentication = BasicAuthentication()
        authorization = Authorization()

    def apply_authorization_limits(self, request, object_list):
        if request.method == 'GET':
            friends = []
            print object_list
            for friend in Friendship.objects.filter(friend=request.user):
                if Friendship.objects.are_friends(friend.user, friend.friend):
                    friends.append(friend)
            return friends

        return object_list.filter(owner=request.user)

class RaceTimesResource(ModelResource):
    class Meta:
        queryset = RaceTime.objects.all()
        resource_name = 'times'

        allowed_methods = ['post']

        authentication = BasicAuthentication()
        authorization = RaceTimesAuth()

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

    def obj_create(self, bundle, request=None, **kwargs):
        body = json.loads(request.body)
        race = Race.objects.get(id=body['race'])
        return super(RaceTimesResource, self).obj_create(bundle, 
                                                         request, 
                                                         user=request.user,
                                                         race=race)

class RaceUsersResource(ModelResource):
    users = fields.ToOneField('raceall.api.backend.AdminUserResource', 'user', full=True)
    times = fields.ToManyField(RaceTimesResource, 'time', full=True)

    class Meta:
        queryset = RaceUser.objects.all()
        resource_name = 'users'

        allowed_methods = ['post', 'delete', 'put']

        authentication = BasicAuthentication()
        authorization = RaceUsersAuth()

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

    def obj_create(self, bundle, request=None, **kwargs):
        body = json.loads(request.body)
        race = Race.objects.get(id=body['race'])
        return super(RaceUsersResource, self).obj_create(bundle,
                                                         request,
                                                         user=request.user,
                                                         race=race)

        

class RaceResource(ModelResource):
    racer = fields.ToManyField(RaceUsersResource, 'users', full=True)

    class Meta:
        queryset = Race.objects.all()
        resource_name = 'race'

        authentication = BasicAuthentication()
        authorization = Authorization()

    def apply_authorization_limits(self, request, object_list):
        if request.method != 'GET':
            return object_list.filter(owner=request.user)


        wanted = set()
        for race in object_list:
            if (race.private == False
               or race.owner == request.user
               or Friendship.objects.are_friends(race.owner, request.user)):
                wanted.add(race.pk)

        return object_list.filter(pk__in = wanted)

    def obj_create(self, bundle, request=None, **kwargs):
        return super(RaceResource, self).obj_create(bundle, request, owner=request.user)
