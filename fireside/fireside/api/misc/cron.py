__all__ = ["cron_pretty"]

from fireside.api import misc_router
from fireside.utils import cron_pretty as _cron_pretty


@misc_router.get("/cron_pretty", url_name="cron_pretty")
async def cron_pretty(request, cron: str) -> str:
    await request.auth  # ensure authentication is awaited
    return _cron_pretty(cron)
