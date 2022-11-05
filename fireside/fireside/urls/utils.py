from ninja import Router
from fireside.utils import cron_pretty as _cron_pretty

import logging

logger = logging.getLogger(__name__)

router = Router()


@router.get(
    "/cron_pretty",
    description="Returns a human readable representation of a cron string",
)
def cron_pretty(request, cron: str) -> str:
    logger.debug(
        f"""
        {request.GET}
        {cron}
    """
    )
    return _cron_pretty(cron)
