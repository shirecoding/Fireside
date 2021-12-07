from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserProfileForm, ReplyMailForm
from .models import Mail
from firesidegames.forms.settings import create_settings_form


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

        # user_settings
        elif "user_settings" in request.POST:
            profile = request.user.profile.first()
            form = create_settings_form(profile.settings)(request.POST)
            if form.is_valid():
                profile.settings = form.settings
                profile.save(update_fields=["settings"])
                return HttpResponseRedirect(reverse("profile_settings:index"))

        # reply_mail
        elif "reply_mail" in request.POST:
            profile = request.user.profile.first()
            form = ReplyMailForm(request.POST)
            if form.is_valid():
                m = Mail.objects.get(pk=form.cleaned_data["mail_id"])
                Mail.objects.create(
                    title=form.cleaned_data["title"],
                    content=form.cleaned_data["content"],
                    from_user=m.user_profile.user,
                    user_profile=m.from_user.profile.first(),
                )
                return HttpResponseRedirect(reverse("profile_settings:index"))

    # index
    elif request.method == "GET":
        profile = request.user.profile.first()
        settings_form = create_settings_form(profile.settings)(None)
        context = {
            "profile": profile,
            "forms": {
                "aboutme": UserProfileForm(instance=profile),
                "user_settings": settings_form,
                "reply_mail": ReplyMailForm(),
            },
            "segment": "profile",
        }
        return render(request, "profile_settings/index.html", context)
