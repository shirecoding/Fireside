__all__ = ["UserSerializer", "UserProfileSerializer"]

from django.contrib.auth.models import User
from profile_settings.models import UserProfileSettings
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileSettings
        fields = ["user", "title", "about"]
