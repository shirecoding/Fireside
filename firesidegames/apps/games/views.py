from django.shortcuts import render
from .models import Game


def index_view(request):

    if request.method == "GET":
        games = Game.objects.all()
        return render(request, "games/index.html", {"games": games, "segment": "games"})


def game_view(request, game):

    if request.method == "GET":

        game = Game.objects.filter(name=game).first()
        props = {
            "url": "ws://127.0.0.1:8080/ws",
            "messages": [],
            "users": [],
            "user": {
                "uid": "benjamin",
                "type": "User",
            },  # TODO: Better way to make dict representation, replace with read data
            "group": {"uid": "gameinstance1", "type": "Group"},
            "rooms": [{"uid": x.uid} for x in game.instances.all()],
        }
        return render(
            request,
            "games/react_mount.html",
            {"component": "js/gameroom.js", "props": props},
        )


def chatroom_view(request):

    if request.method == "GET":
        props = {
            "url": "ws://127.0.0.1:8080/ws",
            "messages": [],
            "users": [],
            "user": {"uid": "benjamin", "type": "User"},
            "group": {"uid": "gameinstance1", "type": "Group"},
        }
        return render(
            request,
            "games/react_mount.html",
            {"component": "js/chatroom.js", "props": props},
        )
