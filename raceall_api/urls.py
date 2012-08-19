from django.conf.urls import patterns, include, url
from django.contrib import admin
from raceall.api.backend import *
from raceall.api.customer import *
from tastypie.api import Api

admin.autodiscover()
customer_api = Api(api_name='customer')
customer_api.register(FriendshipResource())
customer_api.register(FriendshipResource())
customer_api.register(RaceResource())
customer_api.register(RaceUsersResource())
customer_api.register(RaceTimesResource())
#customer_api.register(RaceResource())

admin_api = Api(api_name='admin')
admin_api.register(AdminUserResource())
admin_api.register(AdminRaceResource())
admin_api.register(AdminRaceUsers())
#admin_api.register(AdminRaceTimes())

urlpatterns = patterns('',
    url(r'^api/', include(customer_api.urls)),
    url(r'^api/', include(admin_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
