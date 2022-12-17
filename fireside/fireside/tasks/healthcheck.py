__all = ["ServiceStatus", "ServiceTable", "healthcheck"]
import logging
from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from fireside.utils.task import task

logger = logging.getLogger(__name__)


class ServiceStatus(BaseModel):
    service: str
    status: Literal["up", "down", "pending"] = "pending"
    last_updated: datetime


class ServiceTable(BaseModel):
    services: list[ServiceStatus]


@task(name="Healthcheck", description="Performs system health check")
def healthcheck(service_table: ServiceTable) -> ServiceTable:
    logger.debug(f"Performing Healthcheck")
    return ServiceTable(
        services=[
            ServiceStatus(**entry.pop("status"), status="ok")
            for entry in service_table.services
        ]
    )
