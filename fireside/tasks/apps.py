from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tasks"

    def ready(self):
        """
        TODO:
            - check for invalidated tasks, and delete
        """
        from tasks.utils import remove_invalid_task_definitions, reschedule_all_tasks

        # delete invalid task definitions
        remove_invalid_task_definitions()

        # reschedule all tasks
        reschedule_all_tasks()
