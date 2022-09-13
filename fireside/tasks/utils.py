__all__ = ["register_task", "get_redis_connection"]

import inspect
from django.core.cache.backends.redis import RedisCache
from django.core.cache import caches
from redis.client import Redis


def register_task(name="", description=""):
    """
    Decorator used to register any function as a task.
    Uses type hints to create the schema for the `inputs` field.

    To ensure that tasks are discovered and registered, import tasks in AppConfig.ready

    TODO:
        - add schema based on type hints of function
    """

    from tasks.models import TaskDefinition  # prevent circular imports

    def decorator(f):
        TaskDefinition.objects.update_or_create(
            fpath=f"{inspect.getmodule(f).__name__}.{f.__name__}", defaults={"name": name, "description": description}
        )

        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapper

    return decorator


def get_redis_connection() -> Redis:
    for obj in caches.all():
        if isinstance(obj, RedisCache):
            return obj._cache.get_client()
    raise Exception("Missing RedisCache backend")
