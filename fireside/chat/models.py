import uuid
from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    users = models.ManyToManyField(to=User, blank=True)

    def get_user_count(self):
        return self.users.count()

    def join(self, user):
        self.users.add(user)
        self.save()

    def leave(self, user):
        self.users.remove(user)
        self.save()

    def __str__(self):
        return f"{self.name} ({self.get_user_count()})"


class Message(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content} [{self.timestamp}]"
