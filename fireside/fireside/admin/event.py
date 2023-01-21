from django.contrib import admin

from fireside.admin import ModelAdmin
from fireside.models import EventHandler


class EventHandlerAdmin(ModelAdmin):

    list_display = [
        "event",
        "task",
    ]

    fieldsets = [
        [None, {"fields": ("event", "task")}],
    ]


admin.site.register(EventHandler, EventHandlerAdmin)
