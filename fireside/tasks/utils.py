__all__ = ["register_task", "get_redis_connection", "get_scheduler", "get_worker"]

from django.core.cache.backends.redis import RedisCache
from django.core.cache import caches
from redis.client import Redis
from rq_scheduler import Scheduler
from functools import lru_cache
from fireside.utils import get_function_import_path
from rq import Worker


def register_task(name="", description=""):
    """
    Decorator used to register any function as a task.
    Uses type hints to create the schema for the `inputs` field.

    To ensure that tasks are discovered and registered, import tasks in AppConfig.ready

    TODO:
        - add schema based on type hints of function
    """

    def decorator(f):
        from tasks.models import TaskDefinition  # prevent circular imports

        fpath = get_function_import_path(f)

        if fpath is None:
            raise Exception(f"Failed to register task: import path of {f} cannot be reached")

        TaskDefinition.objects.update_or_create(fpath=fpath, defaults={"name": name, "description": description})

        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapper

    return decorator


@lru_cache
def get_redis_connection() -> Redis:
    for obj in caches.all():
        if isinstance(obj, RedisCache):
            return obj._cache.get_client()
    raise Exception("Missing RedisCache backend")


@lru_cache
def get_scheduler() -> Scheduler:
    return Scheduler(connection=get_redis_connection())


@lru_cache
def get_worker() -> Worker:
    from tasks.models import TaskDefinition  # prevent circular imports

    return Worker({x.queue_name for x in TaskDefinition.objects.all()}, connection=get_redis_connection())
