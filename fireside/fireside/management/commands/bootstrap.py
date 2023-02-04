import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Tasks to perform before the server boots up"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        from fireside.utils.task import remove_invalid_tasks, reschedule_tasks

        # Migrate
        call_command("migrate")

        # Update permissions
        call_command("update_permissions")
        call_command("remove_stale_contenttypes")

        # Clean tasks
        logger.info("Cleaning tasks ...")
        remove_invalid_tasks()
        reschedule_tasks()

        # Create default tasks
        import fireside.events  # noqa
        import fireside.tasks  # noqa
