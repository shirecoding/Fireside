__all = ["ServiceStatus", "PHealthCheck", "health_check"]
import logging
from datetime import datetime
from typing import Literal

from django.db import connection
from django.utils import timezone
from pydantic import BaseModel

from fireside.protocols import Protocol, ProtocolDict
from fireside.utils.task import task

logger = logging.getLogger(__name__)


class ServiceStatus(BaseModel):
    service: str
    status: Literal["up", "down", "pending"] = "pending"
    last_updated: datetime


class PHealthCheck(Protocol):
    protocol: str = "phealthcheck"
    services: list[ServiceStatus]


def check_db() -> Literal["up", "down", "pending"]:
    with connection.cursor() as cursor:
        cursor.execute("select 1")
        one = cursor.fetchone()[0]
        return "down" if one != 1 else "up"
    return "down"


@task(name="HealthCheck", description="Performs system health check")
def health_check(**protocols) -> ProtocolDict:
    logger.debug(f"Performing Healthcheck")
    return PHealthCheck(
        services=[
            ServiceStatus(service="db", status=check_db(), last_updated=timezone.now())
        ]
    )
