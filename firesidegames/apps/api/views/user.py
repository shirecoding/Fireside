__all__ = ["UserProfileDetail", "friend_request"]

from user_profile.models import UserProfile
from rest_framework import generics
from api.serializers import UserProfileSerializer
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import logging
from user_profile.models import UserRelationship, UserProfile
from user_profile.utils import Constants as UserProfileConstants

logger = logging.getLogger(__name__)


class UserProfileDetail(generics.RetrieveAPIView):
    """
    Allow user to retrieve his own user profile
    """

    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().first()


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def friend_request(request):
    """
    Send a friend request
    """

    user_profile = UserProfile.objects.get(user=request.user)
    other_profile = UserProfile.objects.get(user__username=request.data.get("uid"))

    if not UserRelationship.objects.filter(
        user_profile=user_profile, other_profile=other_profile
    ).exists():
        UserRelationship.objects.create(
            user_profile=user_profile,
            other_profile=other_profile,
            relationship_type=UserProfileConstants.UserRelationshipType.friend,
            relationship_state=UserProfileConstants.UserRelationshipState.request,
        )
        UserRelationship.objects.create(
            user_profile=other_profile,
            other_profile=user_profile,
            relationship_type=UserProfileConstants.UserRelationshipType.friend,
            relationship_state=UserProfileConstants.UserRelationshipState.request,
        )

    return Response(request.data)
