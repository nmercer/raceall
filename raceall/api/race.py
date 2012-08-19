from django.contrib.auth.models import User
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL
from raceall.models import Friendship, Race, RaceUsers, RaceTimes

from django.views.decorators.csrf import csrf_exempt

#XXX: TESTING
from tastypie.authorization import Authorization
from auth import *

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {
            'username': ALL,
        }

        authentication = BasicAuthentication()
        authorization = Authorization()

class FriendshipResource(ModelResource):
    users = fields.ToManyField(UserResource, 'user', full=True)

    class Meta:
        queryset = Friendship.objects.all()
        resource_name = 'friends'
        allowed_methods = ['get']

        authentication = BasicAuthentication()
        authorization = Authorization()

    def apply_authorization_limits(self, request, object_list):
        friends = []
        for friend in Friendship.objects.filter(friend=request.user):
            if Friendship.objects.are_friends(friend.user.all(), friend.friend.all()):
                friends.append(friend)

        return friends

#XXX: Need delete to delete all user/time/gps resources, obj_delete?
class RaceResource(ModelResource):
    class Meta:
        queryset = Race.objects.all()
        resource_name = 'race'

        allowed_methods = ['post', 'put', 'delete']

        excludes = ['added']

        authentication = BasicAuthentication()
        authorization = Authorization()

    #Only allow user to modify own resources
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(owner=request.user)

    #Create uses user as owner
    def obj_create(self, bundle, request=None, **kwargs):
        return super(RaceResource, self).obj_create(bundle, request, owner=request.user)

#XXX: Race is Public, Friends with Owner
class RaceUsersResource(ModelResource):
    class Meta:
        queryset = RaceUsers.objects.all()
        resource_name = 'users'

        allowed_methods = ['post', 'delete']

        authentication = BasicAuthentication()
        authorization = RaceUsersAuth()

    #Only allow user to delete own racer
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(racer=request.user)

    #Create uses user as racer
    def obj_create(self, bundle, request=None, **kwargs):
        return super(RaceUsersResource, self).obj_create(bundle, request, racer=request.user)

class RaceTimesResource(ModelResource):
    class Meta:
        queryset = RaceTimes.objects.all()
        resource_name = 'times'

        allowed_methods = ['post']

        authentication = BasicAuthentication()
        authorization = RaceTimesAuth()

    #Create uses user as racer
    def obj_create(self, bundle, request=None, **kwargs):
        return super(RaceTimesResource, self).obj_create(bundle, request, racer=request.user)
