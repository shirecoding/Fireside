from django.contrib import admin
from django.urls import reverse
from chat.models import Room
from django.utils.html import format_html


class ChatRoomAdmin(admin.ModelAdmin):

    list_display = ["name", "user_count", "uid", "chat_room_link"]
    readonly_fields = ["chat_room_link"]

    def chat_room_link(self, obj: Room):
        return format_html(
            '<a href="{}" target="_blank">Join Room</a>',
            reverse("chat-room", current_app="chat", args=[obj.name]),
        )


admin.site.register(Room, ChatRoomAdmin)
