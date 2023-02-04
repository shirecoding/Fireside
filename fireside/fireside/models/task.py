__all__ = ["TaskSchedule", "Task", "TaskPriority", "TaskPreset", "TaskStatus"]

import logging
import traceback
import uuid
from typing import Any, get_type_hints

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django_rq import get_connection, get_queue, get_scheduler
from rq.job import Job
from rq.queue import Queue

from fireside.models import (
    ActivatableModel,
    Model,
    NameDescriptionModel,
    TimestampModel,
)
from fireside.utils import cron_pretty, import_path_to_function

logger = logging.getLogger(__name__)


class TaskPriority(models.TextChoices):
    LOW = "low", "Low"
    DEFAULT = "default", "Default"
    HIGH = "high", "High"


class TaskStatus(models.TextChoices):
    ENQUEUED = "enqueued", "Enqueued"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"


class TaskLog(TimestampModel):

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey("Task", to_field="uid", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=256,
        choices=TaskStatus.choices,
        default=TaskStatus.ENQUEUED,
    )
    started_on = models.DateTimeField(blank=True, null=True)
    completed_on = models.DateTimeField(blank=True, null=True)
    traceback = models.TextField(blank=True, null=True)
    result = models.JSONField(blank=True, null=True)


def on_success(job, connection, result, *args, **kwargs):

    # update task log
    task_log = TaskLog.objects.get(uid=job.kwargs["task_log_uid"])
    task_log.status = TaskStatus.COMPLETED
    task_log.completed_on = timezone.now()
    task_log.result = result
    task_log.save(update_fields=["status", "completed_on", "result"])

    # INFINITE - task_completed_event -> event handler that lists for it runs its task -> task_completed_event
    # # handle `TaskCompleted` event
    # handle_event(
    #     task_completed_event,
    #     task_uid=str(task_log.task.uid),
    #     task_log_uid=str(task_log.uid),
    # )


def on_failure(job, connection, type, value, tb):

    # update task log
    task_log = TaskLog.objects.get(uid=job.kwargs["task_log_uid"])
    task_log.status = TaskStatus.FAILED
    task_log.completed_on = timezone.now()
    task_log.traceback = "".join(traceback.format_tb(tb))
    task_log.save(update_fields=["status", "completed_on", "traceback"])

    # # handle `TaskCompleted` event
    # handle_event(
    #     task_completed_event,
    #     task_uid=str(task_log.task.uid),
    #     task_log_uid=str(task_log.uid),
    # )


class Task(Model, NameDescriptionModel):
    """
    Only `kwargs` are supported
    """

    fpath = models.CharField(
        max_length=256,
        unique=True,
        blank=False,
        null=True,  # when adding, is_valid checks for None
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

    def __repr__(self) -> str:
        return str(self)

    def run(self, *args, task_log_uid: str | None = None, **kwargs):
        """Task function that is run in the worker."""

        if args:
            raise Exception("`Task` support `kwargs` only")

        func = import_path_to_function(self.fpath)
        return func(**kwargs)

    def get_type_hints(self):
        return get_type_hints(import_path_to_function(self.fpath))

    def enqueue(
        self,
        *args,
        priority: TaskPriority | None = None,
        **kwargs,
    ) -> TaskLog:

        # create/update task log
        task_log = TaskLog.objects.create(
            task=self,
            status=TaskStatus.ENQUEUED,
        )
        kwargs["task_log_uid"] = str(task_log.uid)

        get_queue(name=priority or self.priority).enqueue(
            self.run,
            kwargs=kwargs,
            on_success=on_success,
            on_failure=on_failure,
        )

        return task_log

    def delay(self, *args, **kwargs) -> TaskLog:
        return self.enqueue(**kwargs)

    def is_valid(self) -> bool:
        # check if path to function is still valid (could have been deleted)
        try:
            import_path_to_function(self.fpath)
            return True
        except Exception:
            if self.fpath is not None:  # `fpath` is None during creation
                logger.exception(f"Failed to import {self}")
            return False


class TaskPreset(Model, ActivatableModel, NameDescriptionModel):
    """
    Inputs for `Task`s are `kwargs` only, `args` are not supported
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    priority = models.CharField(
        choices=TaskPriority.choices,
        default=TaskPriority.DEFAULT,
        max_length=128,
        help_text="Priority of the task preset (overrides task priority)",
    )
    kwargs = models.JSONField(
        default=dict, blank=True, help_text="Input kwargs for the task"
    )

    def __str__(self):
        return f"{self.name}"

    def __repr__(self) -> str:
        return str(self)

    def run(self) -> Any:
        """Blocking call of the task"""
        if self.is_active:
            return self.task.run(**self.kwargs)

    def enqueue(self) -> TaskLog | None:
        if self.is_active:
            return self.task.enqueue(self.priority, **self.kwargs)

    def delay(self) -> TaskLog | None:
        if self.is_active:
            return self.enqueue()


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

    def get_job(self) -> Job:
        """
        Fetches the internal rq job for this task schedule
        """
        return Job.fetch(self.job_id, connection=get_connection())

    @property
    def job_id(self) -> str:
        return str(self.uid)

    def get_queue(self) -> Queue:
        return get_queue(name=self.priority)

    def run(self) -> Any:
        """
        Blocking call of the task preset
        """
        if self.is_active:
            return self.task_preset.run()

    def enqueue(self) -> TaskLog | None:
        if self.is_active:
            return self.task_preset.enqueue()

    def delay(self) -> TaskLog | None:
        return self.enqueue()

    def schedule(self) -> None:
        logger.debug(f"Schedule {self}")
        get_scheduler(self.priority).cron(
            self.cron,
            id=self.job_id,
            func=self.enqueue,  # enqueue instead of run so that task logs are generated
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
    Unschedules all jobs for this task
    """
    old_instance = sender.objects.filter(uid=instance.uid).first()
    if old_instance:
        old_instance.unschedule()


@receiver(post_save, sender=TaskSchedule, dispatch_uid="post_save_task_schedule")
def post_save_task_schedule(sender, instance, created, *args, **kwargs):
    """
    Reschedules job for this task
    """
    instance.schedule()
