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
from rest_framework.response import Response
import logging
from user_profile.models import UserProfile
from user_profile.utils import Constants as UserProfileConstants
from django.utils.http import is_safe_url
from django.http import HttpResponseRedirect


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


@api_view(["POST", "GET"])
@authentication_classes([SessionAuthentication])
@permission_classes([])
def friend_request(request):
    """
    Send a friend request

    data:
        uid: <user.username>
        method: <create|accept|reject>
    """

    uid = request.data.get("uid") or request.query_params.get("uid")
    method = request.data.get("method") or request.query_params.get("method")
    redirect_url = request.data.get("next") or request.query_params.get("next")

    user_profile = UserProfile.objects.get(user=request.user)
    other_profile = UserProfile.objects.get(user__username=uid)

    # Create a friend request
    if method == "create":
        user_profile.request_user_relationship(
            other_profile, UserProfileConstants.UserRelationshipType.friend
        )

    # Accept a friend request
    elif method == "accept":
        user_profile.accept_user_relationship(
            other_profile, UserProfileConstants.UserRelationshipType.friend
        )

    # Reject a friend request
    elif method == "reject":
        user_profile.reject_user_relationship(
            other_profile, UserProfileConstants.UserRelationshipType.friend
        )

    if redirect_url and is_safe_url(redirect_url, allowed_hosts=request.get_host()):
        return HttpResponseRedirect(redirect_url)

    return Response(request.data)
