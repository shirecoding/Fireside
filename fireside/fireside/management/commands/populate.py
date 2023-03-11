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

        #
        # Create a HealthCheck `TaskPreset`
        #
        health_check_task = Task.objects.get(name="HealthCheck")

        health_check_preset, _ = TaskPreset.objects.update_or_create(
            name="health_check",
            defaults=dict(
                description="Health Check",
                task=health_check_task,
                kwargs={},  # no kwargs for healthcheck
            ),
        )

        # maunally run HealthCheck `TaskPreset` once
        task_log = health_check_preset.delay()

        logger.debug(
            f"""
            uid: {task_log.uid}
            task: {task_log.task}
            status: {task_log.status}
            started_on: {task_log.started_on}
            completed_on: {task_log.completed_on}
            traceback: {task_log.traceback}
            result: {task_log.result}
        """
        )

        #
        # Create an hourly `TaskSchedule` for the HealthCheck `TaskPreset`
        #
        TaskSchedule.objects.update_or_create(
            task_preset=health_check_preset, cron="0 * * * *"  # every hour
        )

        #
        # Create an `EventHandler` for HealthCheckSuccess `Event` which hooks up to StdoutLogger `Task`
        #
        from fireside.models.event import EventHandler
        from fireside.tasks.health_check import health_check_success

        stdout_logger_task = Task.objects.get(name="StdoutLogger")

        log_health_check_success, _ = EventHandler.objects.update_or_create(
            name="LogHealthCheckSuccess",
            defaults=dict(
                description="Logs HealthCheck success to stdout.",
                event=health_check_success,
                task=stdout_logger_task,
            ),
        )

        # check event is logged to stdout debug
        health_check_preset.delay()
