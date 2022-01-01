from django.shortcuts import render
from fsg_agent.utils.message import User, Group
from .models import Game
from dataclasses import asdict
import jwt
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta


def index_view(request):

    if request.method == "GET":
        games = Game.objects.all()
        return render(request, "games/index.html", {"games": games, "segment": "games"})


def game_view(request, game):

    if request.method == "GET":

        game = Game.objects.filter(name=game).first()
        props = {
            "messages": [],
            "users": [],
            "group": asdict(Group(uid=game.name)),
            "rooms": [
                {
                    "uid": x.uid,
                }
                for x in game.instances.all()
            ],
            # context variables
            "url": game.websocket,
            "user": asdict(User(uid=request.user.username)),
            "jwt": jwt.encode(
                {
                    "user": request.user.username,
                    "group": game.name,
                    "exp": timezone.now() + timedelta(minutes=1),
                },
                settings.FSG_JWT_SECRET,
                algorithm="HS256",
            ),
            "api": {
                "websocket": game.websocket,
                "friend_request": request.build_absolute_uri(
                    reverse("api:friend_request")
                ),
            },
        }
        return render(
            request,
            "games/react_mount.html",
            {"component": "js/gameroom.js", "props": props},
        )
