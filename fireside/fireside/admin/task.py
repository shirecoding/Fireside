from django.contrib import admin, messages
from django.forms import ModelForm

from fireside.admin import ModelAdmin
from fireside.models.task import Task, TaskLog, TaskPreset, TaskSchedule
from fireside.utils.widgets import CronTextInput


class TaskScheduleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cron"].widget = CronTextInput()


class TaskScheduleAdmin(ModelAdmin):
    form = TaskScheduleForm
    list_display = [
        "cron_pretty",
        "repeat",
        "priority",
        "timeout",
    ]
    readonly_fields = ["name"]
    actions = ModelAdmin.actions + ["run_tasks"]

    fieldsets = [
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

    list_display = ["fpath", "is_valid", "priority", "timeout"]
    readonly_fields = [
        "name",
        "description",
        "fpath",
        "is_valid",
        "priority",
        "timeout",
    ]


from django_ace import AceWidget


class TaskPresetForm(ModelForm):
    """
    Set the instance on the widget so that the `kwargs` json schema callable may access the `instance`

    https://django-jsonform.readthedocs.io/en/latest/fields-and-widgets.html?highlight=callable#accessing-model-instance-in-callable-schema
    """

    class Meta:
        widgets = {
            "args": AceWidget(
                mode="json",
                theme="twilight",
                width="500px",
                height="100px",
                toolbar=False,
                showgutter=False,
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["kwargs"].widget.instance = self.instance


class TaskPresetAdmin(ModelAdmin):
    form = TaskPresetForm

    list_display = ["task"]
    fieldsets = [
        [
            "Task",
            {
                "fields": (
                    "task",
                    "args",
                    "kwargs",
                )
            },
        ]
    ]


class TaskLogAdmin(admin.ModelAdmin):
    list_display = ["task", "started_on", "completed_on", "status"]


admin.site.register(TaskLog, TaskLogAdmin)
admin.site.register(TaskSchedule, TaskScheduleAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskPreset, TaskPresetAdmin)
