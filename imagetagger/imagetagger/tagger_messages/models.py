from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.db import models
from django.contrib.auth.models import Group
import os

from imagetagger.users.models import Team


class Message(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                             default=None,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    expire_time = models.DateTimeField()
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='read_messages')
    
    def __str__(self):
        return u'Message: {0}'.format(str(self.title))


class TeamMessage(Message):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='message',
    )
    admins_only = models.BooleanField(default=False)

    @staticmethod
    def get_messages_for_user(user):
        userteams = Team.objects.filter(members=user)
        adminteams = userteams
        return TeamMessage.objects.filter(Q(team__in=adminteams, admins_only=True) | Q(team__in=userteams, admins_only=False))

class GlobalMessage(Message):
    team_admins_only = models.BooleanField(default=False)
    staff_only = models.BooleanField(default=False)

    @staticmethod
    def get():
        pass       
    