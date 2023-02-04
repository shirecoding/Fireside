from django.contrib import admin

from fireside.admin import ModelAdmin
from fireside.models.event import Event, EventHandler


class EventAdmin(ModelAdmin):
    # add using `register_event`
    list_display = ["mpath"]
    readonly_fields = ["name", "description", "mpath"]

    fieldsets = [
        [None, {"fields": ["mpath"]}],
    ]


class EventHandlerAdmin(ModelAdmin):

    list_display = [
        "event",
        "task",
    ]

    fieldsets = [
        [None, {"fields": ["event", "task"]}],
    ]


admin.site.register(Event, EventAdmin)
admin.site.register(EventHandler, EventHandlerAdmin)
