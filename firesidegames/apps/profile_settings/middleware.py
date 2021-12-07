from django.utils import timezone
from .models import UserSession


class SetUserSessionLastUpdated(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # update last_updated
        if request.user.is_authenticated:
            user_session = UserSession.objects.get(user=request.user)
            user_session.last_updated = timezone.now()
            user_session.save(update_fields=["last_updated"])
        return self.get_response(request)
