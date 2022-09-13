__all__ = ["Task", "TaskDefinition"]

from fireside.models import Model, ActivatableModel
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.db import models
import importlib
from rq_scheduler import Scheduler
from tasks.utils import get_redis_connection
from rq.queue import Queue

import logging

logger = logging.getLogger(__name__)
scheduler = Scheduler(connection=get_redis_connection())


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
        xs = self.definition.fpath.split(".")
        getattr(importlib.import_module(".".join(xs[:-1])), xs[-1])(*self.inputs["args"], **self.inputs["kwargs"])


@receiver(pre_save, sender=Task, dispatch_uid="pre_save_task")
def pre_save_task(sender, instance, *args, **kwargs):
    old_instance = sender.objects.filter(uid=instance.uid).first()
    if old_instance:
        # delete existing queue
        queue_name = f"Task:{old_instance.name}"
        queue = Queue(name=queue_name, connection=get_redis_connection())
        logger.debug(f"Deleting {len(queue.jobs)} existing jobs in queue {queue_name}")
        queue.delete()


@receiver(post_save, sender=Task, dispatch_uid="post_save_task")
def post_save_task(sender, instance, created, *args, **kwargs):
    # reschedule jobs
    queue_name = f"Task:{instance.name}"
    scheduler.cron(
        instance.cron,
        func=instance.run,
        args=[],
        kwargs={},
        repeat=instance.repeat,
        queue_name=queue_name,
        meta={},
        use_local_timezone=True,
    )
    logger.debug(f"Scheduled {queue_name}")
