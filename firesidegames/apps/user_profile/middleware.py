from django.utils import timezone
from .models import UserProfile


class UpdateUserProfileMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

            # update last_updated
            user_profile.last_updated = timezone.now()
            user_profile.save(update_fields=["last_updated"])

        return self.get_response(request)
