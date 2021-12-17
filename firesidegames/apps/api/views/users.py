__all__ = ["UserList", "UserDetail", "UserProfileDetail"]

from django.contrib.auth.models import User
from profile_settings.models import UserProfileSettings
from rest_framework import generics
from api.serializers import UserSerializer, UserProfileSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    Allow user to retrieve his own user
    """

    serializer_class = UserSerializer
    lookup_field = "username"

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)


class UserProfileDetail(generics.RetrieveAPIView):
    """
    Allow user to retrieve his own user profile
    """

    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfileSettings.objects.filter(
            user__username=self.request.user.username
        )

    def get_object(self):
        return (
            self.get_queryset()
            .filter(user__username=self.kwargs.get("username"))
            .first()
        )
