from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from profile_settings.models import UserProfileSettings, UserSession
from django.contrib.sessions.models import Session


@receiver(post_save, sender=User)
def post_save_user_handler(sender, instance, **kwargs):
    UserProfileSettings.objects.create(user=instance)


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    UserSession.objects.update_or_create(
        user=user,
        defaults={
            "session": Session.objects.get(session_key=request.session.session_key),
            "last_updated": timezone.now,
        },
    )
