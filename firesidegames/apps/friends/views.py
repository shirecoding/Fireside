from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from profile_settings.models import UserProfileSettings
from profile_settings.utils import Constants as ProfileSettingsConstants


@login_required(login_url="accounts/login/")
def index_view(request):

    # index
    if request.method == "GET":
        profile = request.user.profile.first()
        friends = UserProfileSettings.objects.filter(
            user_connections__connection_type=ProfileSettingsConstants.UserConnectionType.friend,
            user_connections__other_profile=profile,
        )

        context = {
            "profile": profile,
            "friends": friends,
            "segment": "friends",
        }
        return render(request, "friends/index.html", context)
