from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import exceptions
import jwt
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request, *args, **kwargs):

        try:
            encoded_jwt = request.data.get("jwt")
            decoded_jwt = jwt.decode(
                encoded_jwt, settings.FSG_JWT_SECRET, algorithms=["HS256"]
            )
        except:
            logger.exception("Invalid JWT")
            raise exceptions.AuthenticationFailed("Invalid JWT")

        username = decoded_jwt.get("user") or decoded_jwt.get("username")

        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("No such user")

        return (user, None)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
