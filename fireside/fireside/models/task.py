__all__ = ["TaskSchedule", "Task", "TaskPriority", "TaskPreset"]

import logging
from typing import Any

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_rq import get_connection, get_queue, get_scheduler
from rq.job import Job
from rq.queue import Queue

from fireside.models import ActivatableModel, Model
from fireside.utils import cron_pretty, import_path_to_function

logger = logging.getLogger(__name__)


class TaskPriority(models.TextChoices):
    LOW = "low", "Low"
    DEFAULT = "default", "Default"
    HIGH = "high", "High"


class Task(Model):
    name = models.CharField(unique=True, max_length=128, blank=False, null=False)
    description = models.TextField(max_length=256, default="")
    fpath = models.CharField(
        max_length=256,
        unique=True,
        blank=False,
        null=False,
        help_text="Path to the function to be run (eg. path.to.function)",
    )
    priority = models.CharField(
        choices=TaskPriority.choices,
        default=TaskPriority.DEFAULT,
        max_length=128,
        help_text="Priority of the task",
    )
    timeout = models.IntegerField(
        blank=True,
        null=True,
        help_text="Timeout of the task in seconds (leave empty to use the default timeout)",
    )

    def __str__(self):
        return f"{self.name} ({self.fpath})"

    def __call__(self, event):
        return self.run(event)

    def run(self, event) -> Any:
        return import_path_to_function(self.fpath)(event)

    def enqueue(self, priority: str, event) -> Job:
        return get_queue(name=priority).enqueue(self.run, event)

    def is_valid(self) -> bool:
        # check if path to function is still valid (could have been deleted)
        try:
            import_path_to_function(self.fpath)
            return True
        except Exception:
            logger.exception(f"Failed to import {self}")
            return False


class TaskPreset(Model, ActivatableModel):
    name = models.CharField(unique=True, max_length=128, blank=False, null=False)
    description = models.TextField(max_length=256, default="")
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    event = models.JSONField(
        default=dict, blank=True, help_text="Preset event for the task"
    )

    def __str__(self):
        return f"{self.name}"

    def __repr__(self) -> str:
        return str(self)

    def run(self) -> Any:
        if self.is_active:
            logger.debug(f"Running TaskPreset {self}")
            return self.task.run(self.event)


class TaskSchedule(Model, ActivatableModel):
    """
    Run tasks on a schedule (cron)
    """

    task_preset = models.ForeignKey("TaskPreset", on_delete=models.CASCADE)
    cron = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="A cron string (e.g. '0 0 * * 0')",
    )
    repeat = models.IntegerField(
        blank=True,
        null=True,
        help_text="Repeat this number of times (None means repeat forever)",
    )
    priority = models.CharField(
        choices=TaskPriority.choices,
        default=TaskPriority.DEFAULT,
        max_length=128,
        help_text="Priority of the task (overrides priority set in task)",
    )
    timeout = models.IntegerField(
        blank=True,
        null=True,
        help_text="Timeout of the task in seconds (leave empty to use the default timeout, overrides priority set in task)",
    )

    def __str__(self) -> str:
        return (
            f"{self.task_preset.name} - {self.cron_pretty} x {self.repeat or 'forever'}"
        )

    def __repr__(self) -> str:
        return str(self)

    @property
    def name(self) -> str:
        return str(self)

    @property
    def cron_pretty(self) -> str:
        return cron_pretty(self.cron)

    @property
    def job_id(self) -> str:
        return str(self.uid)

    def get_job(self) -> Job:
        return Job.fetch(self.job_id, connection=get_connection())

    def get_queue(self) -> Queue:
        return get_queue(name=self.priority)

    def run(self) -> Any:
        if self.is_active:
            return self.task_preset.run()

    def __call__(self) -> Any:
        return self.run()

    def delay(self) -> Job:
        return self.get_queue().enqueue(self.run)

    def schedule(self) -> Job:
        logger.debug(f"Schedule {self}")
        return get_scheduler(self.priority).cron(
            self.cron,
            id=self.job_id,
            func=self.run,
            args=[],
            kwargs={},
            repeat=self.repeat,
            queue_name=self.priority,
            timeout=self.timeout,
            meta={
                "task_uid": str(self.uid),
                "task_name": self.name,
            },
            use_local_timezone=False,
        )

    def unschedule(self) -> None:
        if self.job_id in get_scheduler():
            Job.fetch(self.job_id, connection=get_connection()).delete()
            logger.debug(f"Unschedule {self}")


@receiver(pre_save, sender=TaskSchedule, dispatch_uid="pre_save_task_schedule")
def pre_save_task_schedule(sender, instance, *args, **kwargs):
    """
    Does the following:
        - Unschedules all jobs for this task
    """
    old_instance = sender.objects.filter(uid=instance.uid).first()
    if old_instance:
        old_instance.unschedule()


@receiver(post_save, sender=TaskSchedule, dispatch_uid="post_save_task_schedule")
def post_save_task_schedule(sender, instance, created, *args, **kwargs):
    """
    Does the following:
        - Reschedules job for this task
    """
    instance.schedule()
