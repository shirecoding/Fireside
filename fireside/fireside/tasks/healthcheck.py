import logging

from fireside.utils.task import task

logger = logging.getLogger(__name__)


@task(name="Healthcheck", description="Performs system health check")
def healthcheck(*args, **kwargs):
    logger.debug(
        f"""
    Performing healthcheck
        args: {args}
        kwargs: {kwargs}
    """
    )
