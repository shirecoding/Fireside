from django.shortcuts import render
from .models import Game


def games_view(request):

    if request.method == "GET":
        games = Game.objects.all()
        return render(request, "games/index.html", {"games": games, "segment": "games"})


def chatroom_view(request):

    if request.method == "GET":
        component = "js/chatroom.js"
        props = {
            "url": "ws://127.0.0.1:8080/ws",
            "messages": [],
            "users": [],
            "user": "benjamin",
            "group": "gameroom1",
        }
        return render(
            request, "games/chatroom.html", {"component": component, "props": props}
        )
