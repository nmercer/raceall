from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from raceall.models import *
import json

#XXX: Is race public, or friends with user or owner?
class RaceUsersAuth(Authorization):
    def is_authorized(self, request, object=None):
        return True

#XXX: Prob wont work yet
class RaceTimesAuth(Authorization):
    def is_authorized(self, request, object=None):
        return True


        #body = json.loads(request.body)
        #if RaceUser.objects.get(user=request.user, race=body['race']):
        #    return True
        #return False

#if request.method == 'POST':
#    body = json.loads(request.body)
#class FriendshipAuth(Authorization):
#    def is_authorized(self, request, object=None):
#if request.method == 'POST' or request.method == 'DELETE':
#    body = json.loads(request.body)
