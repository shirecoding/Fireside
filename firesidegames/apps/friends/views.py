from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from user_profile.models import UserProfile
from user_profile.utils import Constants as ProfileSettingsConstants


@login_required()
def index_view(request):

    # index
    if request.method == "GET":
        profile = request.user.profile.first()
        friends = UserProfile.objects.filter(
            user_connections__relationship_type=ProfileSettingsConstants.UserRelationshipType.friend,
            user_connections__other_profile=profile,
        )

        context = {
            "profile": profile,
            "friends": friends,
            "segment": "friends",
        }
        return render(request, "friends/index.html", context)
