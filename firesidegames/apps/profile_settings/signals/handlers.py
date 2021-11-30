from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from profile_settings.models import UserProfileSettings


@receiver(post_save, sender=User)
def post_save_user(sender, instance, **kwargs):
    UserProfileSettings.objects.create(user=instance)
