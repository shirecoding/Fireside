__all__ = ["Task", "TaskDefinition"]

from fireside.models import Model, ActivatableModel
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.db import models
import importlib

from tasks.utils import get_redis_connection, get_scheduler
from rq.queue import Queue
from functools import cached_property
from contextlib import suppress

import logging

logger = logging.getLogger(__name__)


class TaskDefinition(Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    description = models.TextField(max_length=256, default="")
    fpath = models.CharField(
        max_length=256,
        unique=True,
        blank=False,
        null=False,
        help_text="Path to the function to be run (eg. path.to.function)",
    )

    def __str__(self):
        return f"{self.name} ({self.fpath})"

    @property
    def queue_name(self) -> str:
        return f"Task:{self.name}"  # discoverable at compile time (for worker)


def default_task_inputs():
    return {"args": "", "kwargs": {}}


class Task(Model, ActivatableModel):
    """
    TODO:
        - Replace inputs JSONField with SchemaJSONField (validate with task_definitions.<task>.schema)
        - Add cron
        - Display cron as readable string "every saturday 10 pm"
        - Store results, errors
        - Add action
        - queue_name not being used on redis (debug)?
        - add priority
    """

    name = models.CharField(max_length=128, blank=False, null=False)
    description = models.TextField(max_length=256, default="")
    inputs = models.JSONField(
        default=default_task_inputs, help_text="JSON containing the `args` and `kwargs` for `task`"
    )
    definition = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE)
    cron = models.CharField(max_length=128, blank=True, null=True, help_text="A cron string (e.g. '0 0 * * 0')")
    repeat = models.IntegerField(
        blank=True, null=True, help_text="Repeat this number of times (None means repeat forever)"
    )

    def __str__(self):
        return f"{self.name}"

    def run(self):
        logger.info(f"Running task {self.name}")
        xs = self.definition.fpath.split(".")
        getattr(importlib.import_module(".".join(xs[:-1])), xs[-1])(*self.inputs["args"], **self.inputs["kwargs"])

    @property
    def queue_name(self) -> str:
        return self.definition.queue_name  # discoverable at compile time (for worker)

    @cached_property
    def queue(self) -> Queue:
        return Queue(name=self.queue_name, connection=get_redis_connection())

    def start(self):
        logger.debug(
            f"""
        Starting task schedule:
            task: {self.name}
            cron: {self.cron}
            repeat: {self.repeat}
        """
        )
        get_scheduler().cron(
            self.cron,
            func=self.run,
            args=[],
            kwargs={},
            repeat=self.repeat,
            queue_name=self.queue_name,
            meta={},
            use_local_timezone=True,
        )

    def stop(self):
        logger.debug(
            f"""
            Stopping task schedule
                task: {self.name}
                jobs: {len(self.queue.jobs)}
        """
        )
        self.queue.delete()


@receiver(pre_save, sender=Task, dispatch_uid="pre_save_task")
def pre_save_task(sender, instance, *args, **kwargs):
    old_instance = sender.objects.filter(uid=instance.uid).first()
    if old_instance:
        # stop task
        old_instance.stop()


@receiver(post_save, sender=Task, dispatch_uid="post_save_task")
def post_save_task(sender, instance, created, *args, **kwargs):
    # clear cached_property
    with suppress(AttributeError):
        del instance.queue
    # start task
    instance.start()
