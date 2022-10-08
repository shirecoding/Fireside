import pytest
from fireside_tests.models import BasicShipModel
from tasks.models import TaskDefinition
from tasks.models import Task
from tasks.models import TaskPriority
from django_rq import get_scheduler


@pytest.fixture
def task(db) -> None:
    import fireside_tests.tasks  # register the repair ship task


@pytest.fixture
def bsg(db) -> BasicShipModel:
    obj = BasicShipModel.objects.create(name="Battle Star Galactica")
    return obj


def test_task(bsg, task):
    # test create task definition
    td = TaskDefinition.objects.get(name="Repair Ship")
    assert td.name == "Repair Ship"

    # test create task
    t = Task.objects.create(
        name="Repair ship daily",
        description="This task performs daily repairs on a ship at 00:00 for 2 reps",
        definition=td,
        cron="* * * * *",
        repeat=2,
        priority=TaskPriority.LOW,
        inputs={
            "args": str(bsg.uid),
            "kwargs": {},
        },
    )
    assert Task.objects.get(name="Repair ship daily").definition == td

    # test queue
    assert t.get_queue().name == TaskPriority.LOW

    # test job in scheduler
    scheduler = get_scheduler()
    assert t.job_id in scheduler

    # test job
    assert t.get_job().id == t.job_id
