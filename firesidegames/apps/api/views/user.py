__all__ = ["UserProfileDetail"]

from user_profile.models import UserProfile
from rest_framework import generics
from api.serializers import UserProfileSerializer


class UserProfileDetail(generics.RetrieveAPIView):
    """
    Allow user to retrieve his own user profile
    """

    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().first()
