from django.contrib.auth.models import User
from django.db import models

from core.models import Model


class Room(Model):
    name = models.CharField(max_length=128)
    users = models.ManyToManyField(to=User, blank=True)

    def user_count(self):
        return self.users.count()

    def join(self, user):
        self.users.add(user)
        self.save()

    def leave(self, user):
        self.users.remove(user)
        self.save()

    def __str__(self):
        return f"{self.name} ({self.user_count()})"
