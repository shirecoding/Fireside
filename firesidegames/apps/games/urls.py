from django.urls import path

from .views import index_view, game_view

app_name = "games"  # namespace for {% url 'games:index' %} etc..

urlpatterns = [
    path("game/<str:game>", game_view, name="game"),
    path("", index_view, name="index"),
]
