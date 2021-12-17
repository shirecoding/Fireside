from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from user_profile.models import UserProfile
from django.contrib.sessions.models import Session


@receiver(post_save, sender=User)
def post_save_user_handler(sender, instance, created, **kwargs):
    """
    Ensure that UserProfile is created for every User
    """
    if created:
        UserProfile.objects.update_or_create(user=instance)


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    """
    Update session key in UserProfile on login
    """
    UserProfile.objects.update_or_create(
        user=user,
        defaults={
            "session": Session.objects.get(session_key=request.session.session_key),
        },
    )
