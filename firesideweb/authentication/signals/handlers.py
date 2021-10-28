from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login
from allauth.socialaccount import app_settings
from allauth.account.utils import perform_login
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import redirect
from allauth.exceptions import ImmediateHttpResponse


@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    email_address = sociallogin.account.extra_data["email"]
    users = User.objects.filter(email=email_address)
    if users:
        perform_login(
            request, users[0], email_verification=app_settings.EMAIL_VERIFICATION
        )
        raise ImmediateHttpResponse(
            redirect(settings.LOGIN_REDIRECT_URL.format(id=request.user.id))
        )
