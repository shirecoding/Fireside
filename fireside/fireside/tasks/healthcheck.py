from fireside.utils import register_task

import logging

logger = logging.getLogger(__name__)


@register_task(name="Healthcheck", description="Performs system health check")
def healthcheck(*args, **kwargs):
    logger.debug(
        f"""
    Performing healthcheck
        args: {args}
        kwargs: {kwargs}
    """
    )
