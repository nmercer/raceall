from django.contrib.auth.models import User
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL
from raceall.models import Friendship, Race, RaceUsers, RaceTimes

from django.views.decorators.csrf import csrf_exempt

class FriendshipResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {
            'username': ALL,
        }

#XXX: Need delete to delete all user/time/gps resources, obj_delete?
class RaceResource(ModelResource):
    class Meta:
        queryset = Race.objects.all()
        resource_name = 'race'

        #XXX: Why is this acting so weird
        #allowed_methods = ['post', 'put', 'delete']

        excludes = ['added']

        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

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

        #XXX: Undo after testing
        #allowed_methods = ['post', 'delete']

        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

    #Only allow user to delete own racer
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(racer=request.user)

    #Create uses user as racer
    def obj_create(self, bundle, request=None, **kwargs):
        return super(RaceUsersResource, self).obj_create(bundle, request, racer=request.user)

#XXX: User has entry in RaceUsers
class RaceTimesResource(ModelResource):
    class Meta:
        queryset = RaceTimes.objects.all()
        resource_name = 'times'

        #XXX: Undo after testing
        #allowed_methods = ['post']

        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

    #Create uses user as racer
    def obj_create(self, bundle, request=None, **kwargs):
        return super(RaceTimesResource, self).obj_create(bundle, request, racer=request.user)

















    #def wrap_view(self, view):
    #    @csrf_exempt
    #    def wrapper(request, *args, **kwargs):
    #        print 'wrap wrapper'
    #        return json_response({'code': '3'})

    #def get_object_list(self, request, *args, **kwargs):
    #    return Race.objects.filter(user=request.user)

    #def get_list(self, request, **kwargs):
    #    print 'Get_List!'
    #    return self.create_response(request, self.full_dehydrate(bundle.obj))

    #def post_list(self, request, **kwargs):
    #    print 'Post_List!'
    #    return self.create_response(request, self.full_dehydrate(bundle.obj))

    #def put_detail(self, request, **kwargs):
    #    print 'Put_detail'
    #    return self.create_response(request, self.full_dehydrate(bundle.obj))
