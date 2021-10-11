from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("games/", include("games.urls")),
    re_path(r"^admin$", RedirectView.as_view(url="/admin/")),
    path("admin/", admin.site.urls),
    path("", include("authentication.urls")),
    path("", include("home.urls")),
]
