from django.urls import path
from ninja import NinjaAPI
from fireside.utils import cron_pretty as _cron_pretty

api = NinjaAPI()


@api.get("/cron_pretty")
def cron_pretty(request, cron: str):
    return {
        "cron": cron,
        "cron_pretty": _cron_pretty(cron),
    }


urlpatterns = [
    path("api/", api.urls),
]
