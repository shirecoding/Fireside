from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from user_profile.models import UserProfile
from user_profile.utils import Constants as ProfileSettingsConstants


@login_required()
def index_view(request):

    # index
    if request.method == "GET":
        profile = request.user.profile
        friends = UserProfile.objects.filter(
            user_relationships__relationship_type=ProfileSettingsConstants.UserRelationshipType.friend,
            user_relationships__other_profile=profile,
        )

        context = {
            "profile": profile,
            "friends": friends,
            "segment": "friends",
        }
        return render(request, "friends/index.html", context)
