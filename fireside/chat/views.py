from chat.models import Room
from django.shortcuts import render


def index_view(request):
    return render(
        request,
        "chat/index.html",
        {
            "rooms": Room.objects.all(),
        },
    )


def room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(
        request,
        "chat/room.html",
        {
            "room": chat_room,
        },
    )
