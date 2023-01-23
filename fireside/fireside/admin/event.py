from django.contrib import admin

from fireside.admin import ModelAdmin
from fireside.models import Event, EventHandler


class EventAdmin(ModelAdmin):
    ...


class EventHandlerAdmin(ModelAdmin):

    list_display = [
        "event",
        "task",
    ]

    fieldsets = [
        [None, {"fields": ("event", "task")}],
    ]


admin.site.register(Event, EventAdmin)
admin.site.register(EventHandler, EventHandlerAdmin)
