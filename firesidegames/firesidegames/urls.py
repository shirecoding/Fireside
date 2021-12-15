from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    # django admin
    path("admin/", admin.site.urls),
    # django rest framework
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    # custom
    path("games/", include("games.urls")),
    path("polls/", include("polls.urls")),
    path("accounts/", include("allauth.urls")),
    path("profile_settings/", include("profile_settings.urls")),
    path("friends/", include("friends.urls")),
    path("", include("home.urls")),
]
