from django.apps import AppConfig
from fireside.utils.threading import run_in_daemon_thread
from tasks.utils import get_scheduler, get_worker


class TasksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tasks"

    def ready(self):
        # start scheduler
        run_in_daemon_thread(get_scheduler().run, forever=True)

        # start worker
        run_in_daemon_thread(get_worker().work, forever=True)
