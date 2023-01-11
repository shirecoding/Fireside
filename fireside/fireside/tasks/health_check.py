__all = ["ServiceStatus", "health_check"]
import logging
from datetime import datetime
from typing import Literal

from django.db import connection
from django.utils import timezone
from pydantic import BaseModel

from fireside.utils import JSONObject
from fireside.utils.task import task

logger = logging.getLogger(__name__)


class ServiceStatus(BaseModel):
    service: str
    status: Literal["up", "down", "pending"] = "pending"
    last_updated: datetime


def check_db() -> Literal["up", "down", "pending"]:
    with connection.cursor() as cursor:
        cursor.execute("select 1")
        one = cursor.fetchone()[0]
        return "down" if one != 1 else "up"
    return "down"


@task(name="HealthCheck", description="Performs system health check")
def health_check() -> JSONObject:
    logger.debug("Performing Healthcheck")
    return {
        "services": [
            ServiceStatus(service="db", status=check_db(), last_updated=timezone.now())
        ]
    }
