from django.test import TestCase
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from raceall.models import *

class QueueResourceTest(ResourceTestCase):
    fixtures = ['test_entries.json']

    def setUp(self):
        super(QueueResourceTest, self).setUp()

        # Create user0, user1
        self.username = 'user0'
        self.password = 'user0'
        self.email = 'user0@user.com'
        self.user0 = User.objects.create_user(self.username, self.email, self.password)
        self.user0.save()

        self.username = 'user1'
        self.password = 'user1'
        self.email = 'user1@user.com'
        self.user1 = User.objects.create_user(self.username, self.email, self.password)
        self.user1.save()

        # Create race0, race1
        self.race0 = Race(name='Race0',
                          vehicle='Motorcycle',
                          description='Do it quick yo',
                          owner=self.user0,
                          private=False)
        self.race0.save()

        self.race1 = Race(name='Race1',
                          vehicle='GSXR-750',
                          description='Two wheels bro',
                          owner=self.user1,
                          private=False)
        self.race1.save()

        #Create friendships
        self.friend0 = Friendship(friend=self.user0,user=self.user1)
        self.friend0.save()
        self.friend0 = Friendship(friend=self.user1,user=self.user0)
        self.friend0.save()

        self.racetime0 = RaceTime(time='123.4', user=self.user0, race=self.race0)
        self.racetime0.save()

    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)

    def test_add_user_to_race_unauthorzied(self):
        post_data = {'race':self.race0.pk}
        self.assertHttpUnauthorized(self.api_client.post('/api/customer/users/',
                                                    format='json',
                                                    data=post_data))


    def test_add_user_to_race(self):
        post_data = {'race':self.race0.pk}

        self.assertHttpCreated(self.api_client.post('/api/customer/users/',
                                                    format='json',
                                                    data=post_data,
                                                    authentication=self.get_credentials()))

    def test_add_time_to_race_unauthorzied(self):
        post_data = {'race':self.race0.pk,
                     'time':12.45}

        self.assertHttpUnauthorized(self.api_client.post('/api/customer/times/',
                                                         format='json',
                                                         data=post_data))

    def test_add_time_to_race(self):
        post_data = {'race':self.race0.pk,
                     'time':12.45}

        self.assertHttpCreated(self.api_client.post('/api/customer/times/',
                                                    format='json',
                                                    data=post_data,
                                                    authentication=self.get_credentials()))

    def test_add_friendship(self):
        self.friend0.delete()
        post_data = {'friend':self.user1.pk}

        self.assertHttpCreated(self.api_client.post('/api/customer/friends/',
                                                    format='json',
                                                    data=post_data,
                                                    authentication=self.get_credentials()))

    def test_remove_friendship(self):
        print '$$$$$$$'
        print self.friend0.pk
        self.assertHttpAccepted(self.api_client.delete('/api/customer/friends/12/',
                                                       format='json',
                                                       authentication=self.get_credentials()))
