from django.urls import path

from .views import games_view

urlpatterns = [
    path("", games_view, name="games"),
]
