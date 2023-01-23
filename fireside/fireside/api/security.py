__all__ = ["django_auth_async", "django_auth_superuser_async"]

from asgiref.sync import sync_to_async
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest


async def django_auth_async(request: HttpRequest):
    """
    Default django cookie based authentication
    """

    is_authenticated = await sync_to_async(lambda: request.user.is_authenticated)()
    if not is_authenticated:
        raise PermissionDenied()

    return is_authenticated


async def django_auth_superuser_async(request: HttpRequest):
    """
    Default django cookie based authentication
    """
    is_authenticated = (
        await sync_to_async(lambda: request.user.is_authenticated)()
        and await sync_to_async(lambda: request.user.is_superuser)()
    )

    if not is_authenticated:
        raise PermissionDenied()

    return is_authenticated
