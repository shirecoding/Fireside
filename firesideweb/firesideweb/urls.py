from django.contrib import admin
from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("authentication.urls")),
    path("polls/", include("polls.urls")),
    path("games/", include("games.urls")),
    path("", views.index, name="home"),  # home page
    re_path(r"^.*\.*", views.pages, name="pages"),  # matche any html file
]
