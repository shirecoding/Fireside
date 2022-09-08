from django.urls import reverse
from chat.models import Room
from django.utils.html import format_html
from fireside.admin import ModelAdmin
from django.contrib import admin


class ChatRoomAdmin(ModelAdmin):

    list_display = ["name", "user_count", "uid", "chat_room_link"]
    readonly_fields = ["chat_room_link", "user_count", "uid"]
    fieldsets = [
        (
            "Room",
            {
                "fields": ["name", "description"],
            },
        ),
        ("Details", {"fields": ["user_count", "users", "chat_room_link", "uid"]}),
    ]

    def chat_room_link(self, obj: Room) -> str:
        if obj.name:  # check empty instance
            return format_html(
                '<a href="{}" target="_blank">Join Room</a>',
                reverse("chat-room", current_app="chat", args=[obj.name]),
            )
        return ""


admin.site.register(Room, ChatRoomAdmin)
