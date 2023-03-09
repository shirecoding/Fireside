import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Populate database with initial data for example & testing"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        from fireside.models.task import Task, TaskPreset, TaskSchedule

        # Bootstrap
        logger.info("Bootstrapping ...")
        call_command("bootstrap")

        health_check_task = Task.objects.get(name="HealthCheck")

        health_check_preset, _ = TaskPreset.objects.update_or_create(
            name="health_check",
            defaults=dict(
                description="Health Check",
                task=health_check_task,
                kwargs={},  # no kwargs for healthcheck
            ),
        )

        TaskSchedule.objects.update_or_create(
            task_preset=health_check_preset, cron="0 * * * *"  # every hour
        )
