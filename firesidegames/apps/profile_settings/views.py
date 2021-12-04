from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserProfileForm


@login_required(login_url="accounts/login/")
def index_view(request):

    # process forms
    if request.method == "POST":

        # aboutme
        if "aboutme" in request.POST:
            profile = request.user.profile.first()
            form = UserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("profile_settings:index"))

    # index
    elif request.method == "GET":
        profile = request.user.profile.first()
        context = {
            "profile": profile,
            "forms": {"aboutme": UserProfileForm(instance=profile)},
        }
        return render(request, "profile_settings/index.html", context)
