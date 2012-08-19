import datetime

from django.db import models
from django.contrib.auth.models import User

class FriendshipManager(models.Manager):
    def are_friends(self, user1, user2):
        if (self.filter(friend=user1, user=user2).count() > 0 and
            self.filter(friend=user2, user=user1).count() > 0):
            return True
        return False

class Friendship(models.Model):
    friend = models.ForeignKey(User, related_name="friend")
    user = models.ForeignKey(User, related_name="user")
    objects = FriendshipManager()

    class Meta:
        unique_together = (("user", "friend"),)
    
    def __unicode__(self):
        return str(self.id)

class RaceTime(models.Model):
    time = models.FloatField()
    race = models.ForeignKey('Race')
    user = models.ForeignKey(User)

    def __unicode__(self):
        return str(self.id)

class RaceUser(models.Model):
    user = models.ForeignKey(User)
    race = models.ForeignKey('Race')
    time = models.ManyToManyField(RaceTime, blank=True)

    class Meta:
        unique_together = (("user", "race"),)

    def __unicode__(self):
        return str(self.id)

class Race(models.Model):
    name = models.CharField(max_length=30)
    vehicle = models.CharField(max_length=30)
    description = models.CharField(max_length=300, blank=True)
    owner = models.ForeignKey(User)
    private = models.BooleanField()
    added =  models.DateField(default=datetime.date.today)
    users = models.ManyToManyField(RaceUser, related_name='users+', blank=True)

    def __unicode__(self):
        return self.name
