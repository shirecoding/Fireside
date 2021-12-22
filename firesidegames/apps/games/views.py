from django.shortcuts import render
from fsg_agent.utils.message import User, Group
from .models import Game
from dataclasses import asdict


def index_view(request):

    if request.method == "GET":
        games = Game.objects.all()
        return render(request, "games/index.html", {"games": games, "segment": "games"})


def game_view(request, game):

    if request.method == "GET":

        game = Game.objects.filter(name=game).first()
        props = {
            "url": game.websocket,
            "messages": [],
            "users": [],
            "user": asdict(User(uid=request.user.username)),
            "group": asdict(Group(uid=game.name)),
            "rooms": [{"uid": x.uid} for x in game.instances.all()],
        }
        return render(
            request,
            "games/react_mount.html",
            {"component": "js/gameroom.js", "props": props},
        )
