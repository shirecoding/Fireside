from django.apps import AppConfig


class FiresideConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fireside"

    def ready(self):
        import fireside.tasks  # noqa

        # from fireside.utils.tasks import remove_invalid_task_definitions, reschedule_all_tasks

        # # delete invalid task definitions
        # remove_invalid_task_definitions()

        # # reschedule all tasks
        # reschedule_all_tasks()
