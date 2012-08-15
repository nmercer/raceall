import datetime

from django.db import models
from django.contrib.auth.models import User

class FriendshipManager(models.Manager):
    
    def friends_for_user(self, user):
        friends = []
        for friendship in self.filter(from_user=user).select_related(depth=1):
            friends.append({"friend": friendship.to_user, "friendship": friendship})
        for friendship in self.filter(to_user=user).select_related(depth=1):
            friends.append({"friend": friendship.from_user, "friendship": friendship})
        return friends
    
    def are_friends(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2).count() > 0:
            return True
        if self.filter(from_user=user2, to_user=user1).count() > 0:
            return True
        return False
    
    def remove(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2):
            friendship = self.filter(from_user=user1, to_user=user2)
        elif self.filter(from_user=user2, to_user=user1):
            friendship = self.filter(from_user=user2, to_user=user1)
        friendship.delete()

class Friendship(models.Model):
    to_user = models.ForeignKey(User, related_name="friends")
    from_user = models.ForeignKey(User, related_name="_unused_")
    added = models.DateField(default=datetime.date.today)
    
    objects = FriendshipManager()
    
    class Meta:
        unique_together = (('to_user', 'from_user'),)

class Race(models.Model):
    name = models.CharField(max_length=30)
    vehicle = models.CharField(max_length=30)
    description = models.CharField(max_length=300, blank=True)
    owner = models.ForeignKey(User)
    added =  models.DateField(default=datetime.date.today)
    private = models.BooleanField()

#XXX: Needs to be one-to-one
class RaceUsers(models.Model):
    racer = models.ForeignKey(User)
    race = models.ForeignKey(Race)

class RaceTimes(models.Model):
    racer = models.ForeignKey(User)
    race = models.ForeignKey(Race)
    time = models.FloatField()
