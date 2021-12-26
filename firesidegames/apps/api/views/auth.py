from rest_framework.views import APIView
from rest_framework.response import Response
from user_profile.models import UserProfile
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed


class AuthenticateUser(APIView):
    """
    Session authentication for external services

    POST {
        username:
        session:
    }
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):

        if UserProfile.objects.filter(
            user__username=request.data["username"],
            session__session_key=request.data["session"],
            session__expire_date__gte=timezone.now(),
        ).exists():
            return Response(request.data)
        else:
            raise AuthenticationFailed(detail=request.data)
