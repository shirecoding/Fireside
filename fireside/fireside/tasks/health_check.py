__all = [
    "ServiceStatus",
    "Services",
    "health_check",
    "health_check_success",
    "health_check_failure",
]
import logging
from typing import Literal

from django.db import connection
from django.utils import timezone
from pydantic import BaseModel

from fireside.utils import JSONObject
from fireside.utils.event import handle_event, register_event
from fireside.utils.task import task

logger = logging.getLogger(__name__)


class ServiceStatus(BaseModel):
    service: str
    status: Literal["up", "down", "pending"] = "pending"
    last_updated: str | None = None


class Services(BaseModel):
    services: list[ServiceStatus]


def check_db() -> Literal["up", "down", "pending"]:
    with connection.cursor() as cursor:
        cursor.execute("select 1")
        one = cursor.fetchone()[0]
        return "down" if one != 1 else "up"
    return "down"


health_check_success = register_event(
    "HealthCheckSuccess",
    Services,
    description="`Event` when a `HealthCheck` is completed successfully.",
)


health_check_failure = register_event(
    "HealthCheckFailure",
    Services,
    description="`Event` when a `HealthCheck` is unsuccessful.",
)


@task(name="HealthCheck", description="Performs system health check")
def health_check() -> JSONObject:
    logger.debug("Performing Healthcheck")

    services = Services(
        services=[
            ServiceStatus(
                service="db", status=check_db(), last_updated=timezone.now().isoformat()
            )
        ]
    )

    services_d = services.dict()

    # handle events
    if any(s.status == "down" for s in services.services):
        handle_event(health_check_failure, **services_d)
    else:
        handle_event(health_check_success, **services_d)

    return services_d
