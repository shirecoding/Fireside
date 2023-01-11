from django.contrib import admin, messages
from django.forms import ModelForm

from fireside.admin import ModelAdmin
from fireside.models import Task, TaskPreset, TaskSchedule
from fireside.utils.widgets import CronTextInput


class TaskScheduleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cron"].widget = CronTextInput()


class TaskScheduleAdmin(ModelAdmin):
    form = TaskScheduleForm
    list_display = [
        "name",
        "cron_pretty",
        "repeat",
        "is_active",
        "priority",
        "timeout",
    ]
    readonly_fields = ["is_active"]
    actions = ModelAdmin.actions + ["run_tasks"]

    fieldsets = [
        [None, {"fields": ("name",)}],
        ["Task", {"fields": ("task_preset",)}],
        [
            "Schedule",
            {
                "fields": (
                    "cron",
                    "repeat",
                    "priority",
                )
            },
        ],
        [
            "Activation",
            {
                "fields": (
                    "is_active",
                    "activate_on",
                    "deactivate_on",
                )
            },
        ],
    ]

    @admin.action(description="Run selected tasks")
    def run_tasks(self, request, qs):
        if qs:
            jobs = [t.delay() for t in qs]
            messages.add_message(request, messages.INFO, f"Queued {jobs} for running")


class TaskAdmin(ModelAdmin):
    """
    Use `fireside.utils.task.task` to register a Task
    """

    list_display = ["name", "description", "fpath", "is_valid", "priority", "timeout"]
    readonly_fields = [
        "name",
        "uid",
        "description",
        "fpath",
        "is_valid",
        "priority",
        "timeout",
    ]


class TaskPresetAdmin(ModelAdmin):
    list_display = ["name", "description", "task"]
    fieldsets = [
        [
            None,
            {
                "fields": (
                    "name",
                    "task",
                    "kwargs",
                )
            },
        ]
    ]


admin.site.register(TaskSchedule, TaskScheduleAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskPreset, TaskPresetAdmin)
