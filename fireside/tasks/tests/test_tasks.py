import pytest
from fireside_tests.models import BasicShipModel
from tasks.models import TaskDefinition
from tasks.models import Task
from tasks.utils import register_task
from django.utils import timezone
from datetime import datetime
from tasks.models import TaskPriority
from django_rq import get_scheduler


@pytest.fixture
def repair_task(db) -> None:
    @register_task(name="Service Ship", description="Conducts repairs on ship")
    def repair_ship_task(ship_uid: str, last_serviced_on: datetime | None) -> str:
        ship = BasicShipModel.objects.get(uid=ship_uid)
        t = timezone.now() if last_serviced_on is None else last_serviced_on
        ship.last_serviced_on = t
        ship.save(update_fields=["last_serviced_on"])
        return ship_uid


@pytest.fixture
def bsg(db) -> BasicShipModel:
    obj = BasicShipModel.objects.create(name="Battle Star Galactica")
    return obj


def test_task(bsg, repair_task):
    # test create task definition
    td = TaskDefinition.objects.get(name="Service Ship")
    assert td.name == "Service Ship"

    # test create task
    t = Task.objects.create(
        name="Service ship daily",
        description="This task performs daily repairs on a ship at 00:00 for 2 reps",
        definition=td,
        cron="0 0 * * *",
        repeat=2,
        priority=TaskPriority.LOW,
    )
    assert Task.objects.get(name="Service ship daily").definition == td

    # test queue
    assert t.get_queue().name == TaskPriority.LOW

    # test job in scheduler
    scheduler = get_scheduler()
    assert t.job_id in scheduler

    # test job
    assert t.get_job().id == t.job_id
