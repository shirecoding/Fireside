from django.core.management.base import BaseCommand
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Tasks to perform before the server boots up"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        from fireside.utils.task import remove_invalid_tasks, reschedule_tasks

        # Clean tasks
        logger.info("Cleaning tasks ...")
        remove_invalid_tasks()
        reschedule_tasks()
