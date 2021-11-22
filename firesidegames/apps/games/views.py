from django.shortcuts import render
from .models import Game


def index_view(request):

    if request.method == "GET":
        games = Game.objects.all()
        return render(request, "games/index.html", {"games": games, "segment": "games"})


def game_view(request, game):

    if request.method == "GET":

        return render(
            request, "games/game.html", {"game": Game.objects.filter(name=game).first()}
        )


def chatroom_view(request):

    if request.method == "GET":
        component = "js/chatroom.js"
        props = {
            "url": "ws://127.0.0.1:8080/ws",
            "messages": [],
            "users": [],
            "user": {"uid": "benjamin", "type": "User"},
            "group": {"uid": "gameinstance1", "type": "Group"},
        }
        return render(
            request, "games/chatroom.html", {"component": component, "props": props}
        )
