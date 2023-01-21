__all__ = ["CronTextInput"]

from django.urls import reverse_lazy

from .base import FiresideTextInput


class CronTextInput(FiresideTextInput):
    hint_callback = reverse_lazy("fireside:cron_pretty")
