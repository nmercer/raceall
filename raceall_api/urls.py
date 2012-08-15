from django.conf.urls import patterns, include, url
from django.contrib import admin
from raceall.api.resources import FriendshipResource, RaceResource
from tastypie.api import Api

admin.autodiscover()
customer_api = Api(api_name='customer')
customer_api.register(FriendshipResource())
customer_api.register(RaceResource())

urlpatterns = patterns('',
    url(r'^api/', include(customer_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
