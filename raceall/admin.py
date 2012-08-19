from django.contrib import admin
from raceall.models import *

#class RaceUsersAdmin(admin.ModelAdmin):
#    list_display = ['id', 'racer', 'race']

class RaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'vehicle', 'private'] #XXX: owner

#class FriendshipAdmin(admin.ModelAdmin):
#    list_display = ['id', 'to_user', 'from_user']


admin.site.register(RaceUser)
admin.site.register(Race, RaceAdmin)
admin.site.register(Friendship)
admin.site.register(RaceTime)
