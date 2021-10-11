from django.shortcuts import render
from .models import Game


def games_view(request):

    if request.method == "GET":

        games = Game.objects.all()
        return render(request, "games/index.html", {"games": games, "segment": "games"})
