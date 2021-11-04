from django.urls import path

from .views import games_view, chatroom_view

urlpatterns = [
    path("chatroom/", chatroom_view, name="chatroom"),
    path("", games_view, name="games"),
]
