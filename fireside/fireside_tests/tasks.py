from fireside_tests.models import BasicShipModel
from tasks.utils import register_task
from django.utils import timezone
from datetime import datetime


@register_task(name="Repair Ship", description="Conducts repairs on ship")
def repair_ship_task(ship_uid: str, last_serviced_on: datetime | None) -> str:
    ship = BasicShipModel.objects.get(uid=ship_uid)
    t = timezone.now() if last_serviced_on is None else last_serviced_on
    ship.last_serviced_on = t
    ship.save(update_fields=["last_serviced_on"])
    return ship_uid
