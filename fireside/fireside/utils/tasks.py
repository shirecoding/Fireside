__all__ = ["task", "remove_invalid_task_definitions", "reschedule_all_tasks"]

from fireside.utils import function_to_import_path
from django_rq import get_scheduler
import logging

logger = logging.getLogger(__name__)


def task(name="", description=""):
    """
    Decorator used to register any function as a task.

    Uses type hints to create the schema for the `inputs` field.
    To ensure that tasks are discovered and registered, import tasks in AppConfig.ready.
    """

    def decorator(f):
        try:
            from fireside.models import TaskDefinition  # prevent circular imports

            fpath = function_to_import_path(f)

            if fpath is None:
                raise Exception(
                    f"Failed to register task: import path of {f} cannot be reached"
                )

            logger.debug(f"Registering Task:{name} ({fpath})")
            TaskDefinition.objects.update_or_create(
                fpath=fpath, defaults={"name": name, "description": description}
            )

            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)

            return wrapper
        except:
            logger.exception(
                f"Failed to register task: {name} ({fpath}), make sure models are migrated"
            )

    return decorator


def remove_invalid_task_definitions():
    """
    Remove task definitions which are no longer importable
    """
    from fireside.models import TaskDefinition  # prevent circular imports

    for td in TaskDefinition.objects.all():
        if not td.is_valid():
            td.delete()


def reschedule_all_tasks():
    from fireside.models import Task

    # delete all jobs in scheduler
    scheduler = get_scheduler()
    for job in scheduler.get_jobs():
        logger.debug(f"Deleting Job:{job}")
        job.delete()

    # reschedule all tasks (even those which are not active)
    for task in Task.objects.all():
        task.schedule()
