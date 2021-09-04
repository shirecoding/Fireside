from django.contrib import admin
from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("polls/", include("polls.urls")),
    path("", include("authentication.urls")),
    path("", views.index, name="home"),  # The home page
    re_path(r"^.*\.*", views.pages, name="pages"),  # Matches any html file
]
