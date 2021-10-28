from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    re_path(r"^admin$", RedirectView.as_view(url="/admin/")),
    path("admin/", admin.site.urls),
    path("games/", include("games.urls")),
    path("polls/", include("polls.urls")),
    path("accounts/", include("allauth.urls")),
    path("", include("home.urls")),
]
