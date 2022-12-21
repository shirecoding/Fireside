__all__ = ["task", "remove_invalid_tasks", "reschedule_tasks", "get_task_result"]

import logging
from time import sleep

from django_rq import get_scheduler
from rq.job import Job

from fireside.models import TaskPriority
from fireside.protocols import ProtocolDict
from fireside.utils import function_to_import_path

logger = logging.getLogger(__name__)

TIME_STEP = 0.1


def get_task_result(job: Job, timeout=60) -> ProtocolDict:
    """
    Blocking wait for job results
    """

    # poll job status
    time_elapsed = 0
    status = job.get_status(refresh=True)
    while (
        status not in {"finished", "stopped", "canceled", "failed"}
        and time_elapsed < timeout
    ):
        sleep(TIME_STEP)
        time_elapsed += TIME_STEP
        status = job.get_status(refresh=True)

    if time_elapsed > timeout:
        raise Exception(f"`get_job_result` timed out after {timeout}s")

    if status != "finished":
        raise Exception(f"{job} failed with status: {status}")

    return job.result


def task(
    name: str = "",
    description: str = "",
    priority: TaskPriority = TaskPriority.DEFAULT,
    timeout: int | None = None,
):
    """
    Decorator used to register any function as a task.

    Uses type hints to create the schema for the `inputs` field.
    """

    def decorator(f):
        try:
            from fireside.models import Task  # prevent circular imports

            fpath = function_to_import_path(f)

            if fpath is None:
                raise Exception(
                    f"Failed to register task: import path of {f} cannot be reached"
                )

            logger.debug(f"Registering Task: {name} ({fpath})")

            # create/update task with unique name
            Task.objects.update_or_create(
                name=name,
                defaults={
                    "name": name,
                    "fpath": fpath,
                    "description": description,
                    "priority": priority,
                    "timeout": timeout,
                },
            )

            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)

            return wrapper
        except:
            logger.exception(
                f"Failed to register task: {name} ({fpath}), make sure models are migrated"
            )

    return decorator


def remove_invalid_tasks():
    """
    Remove tasks which are no longer importable
    """
    from fireside.models import Task  # prevent circular imports

    for t in Task.objects.all():
        if not t.is_valid():
            logger.debug(f"Deleting invalid task: {t}")
            t.delete()


def reschedule_tasks():
    from fireside.models import TaskSchedule

    # delete all jobs in scheduler
    scheduler = get_scheduler()
    for job in scheduler.get_jobs():
        logger.debug(f"Deleting Job:{job}")
        job.delete()

    # reschedule all tasks (even those which are not active)
    for task in TaskSchedule.objects.all():
        task.schedule()
