__all__ = ["CronTextInput"]

from .base import FiresideTextInput
from .api import router
from fireside.utils import cron_pretty as _cron_pretty
from django.urls import reverse_lazy


@router.get("/cron_pretty", url_name="cron_pretty")
def cron_pretty(request, cron: str) -> str:
    return _cron_pretty(cron)


class CronTextInput(FiresideTextInput):
    hint_callback = reverse_lazy("fireside:cron_pretty")
