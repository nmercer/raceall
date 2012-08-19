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

    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)

    def test_add_user_to_race(self):
        post_data = {'race':self.race0.pk}

        self.assertHttpCreated(self.api_client.post('/api/customer/users/',
                                                    format='json',
                                                    data=post_data,
                                                    authentication=self.get_credentials()))
    def test_add_time_to_race(self):
        post_data = {'race':self.race0.pk,
                     'time':12.45}

        print post_data

        self.assertHttpCreated(self.api_client.post('/api/customer/times/',
                                                    format='json',
                                                    data=post_data,
                                                    authentication=self.get_credentials()))


    #def test_post2(self):
    #    print Friendship.objects.count()
    #    print '/api/customer/friends/{0}/'.format(self.friend0.id)
    #    self.assertHttpAccepted(self.api_client.delete('/api/customer/friends/{0}/'.format(self.friend0.id),
    #                                                   format='json',
    #                                                   authentication=self.get_credentials()))
    #    print Friendship.objects.count()


    #def test_get_queue(self):
    #    resp = self.api_client.get('/api/customer/race/',
    #                               format='json', 
    #                               authentication=self.get_credentials())
    #    self.assertValidJSONResponse(resp)

    #def test2_post1(self):
    #    self.post_data = {'racer':'/api/customer/user/{0}/'.format(self.user1.pk),
    #                      'race':'/api/customer/race/{0}/'.format(self.user0.pk)}

    #    self.assertHttpCreated(self.api_client.post('/api/customer/users/',
    #                                                format='json',
    #                                                data=self.post_data,
    #                                                authentication=self.get_credentials()))



    '''
    def test_get_queue_unauthorzied(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/singleplats/queue/', format='json'))

    def test_get_queue(self):
        resp = self.api_client.get('/api/singleplats/queue/',
                                   format='json', 
                                   authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)
        self.assertEqual(len(self.deserialize(resp)['objects'][0]), 5)

    def test_post_queue_unauthorzied(self):
        self.assertHttpUnauthorized(self.api_client.post('/api/singleplats/queue/', 
                                                         format='json',
                                                         data=self.post_data))

    def test_post_queue(self):
        self.assertEqual(Queue.objects.count(), 1)
        self.assertHttpCreated(self.api_client.post('/api/singleplats/queue/',
                                                    format='json', 
                                                    data=self.post_data, 
                                                    authentication=self.get_credentials()))
        self.assertEqual(Queue.objects.count(), 2)


    def test_put_queue_unauthorzied(self):
        self.assertHttpUnauthorized(self.api_client.put('/api/singleplats/queue/{0}/'.format(self.queue.pk),
                                                         format='json',
                                                         data=self.put_data))

    def test_put_queue_when_at_max_rentals(self):
        self.queue.rented = True
        self.queue.save()
        self.queue2 = Queue(user=self.user, record=self.record2, rented=True)
        self.queue2.save()

        self.assertHttpUnauthorized(self.api_client.put('/api/singleplats/queue/{0}/'.format(self.queue.pk),
                                                        format='json',
                                                        data=self.put_data,
                                                        authentication=self.get_credentials()))

    def test_put_queue(self):
        self.assertEqual(Queue.objects.count(), 1)
        self.assertHttpAccepted(self.api_client.put('/api/singleplats/queue/{0}/'.format(self.queue.pk),
                                                    format='json', 
                                                    data=self.put_data, 
                                                    authentication=self.get_credentials()))
        self.assertEqual(Queue.objects.count(), 1)
        self.assertEqual(Queue.objects.get(pk=self.queue.pk).rented, True)


    def test_delete_queue_unauthorzied(self):
        self.assertHttpUnauthorized(self.api_client.delete('/api/singleplats/queue/{0}/'.format(self.queue.pk),
                                                           format='json'))
    def test_delete_queue_when_rented(self):
        self.queue.rented = True
        self.queue.save()
        self.assertHttpUnauthorized(self.api_client.delete('/api/singleplats/queue/{0}/'.format(self.queue.pk),
                                                       format='json', 
                                                       authentication=self.get_credentials()))

    def test_delete_queue(self):
        self.assertEqual(Queue.objects.count(), 1)
        self.assertHttpAccepted(self.api_client.delete('/api/singleplats/queue/{0}/'.format(self.queue.pk),
                                                       format='json', 
                                                       authentication=self.get_credentials()))
        self.assertEqual(Queue.objects.count(), 0)
    '''
