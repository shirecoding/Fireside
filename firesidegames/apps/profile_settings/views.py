from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="accounts/login/")
def index_view(request):

    context = {"profile": request.user.profile.first()}

    if request.method == "GET":
        return render(request, "profile_settings/index.html", context)
