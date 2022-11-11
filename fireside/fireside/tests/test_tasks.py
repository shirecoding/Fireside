import pytest
from fireside_tests.models import BasicShipModel
from fireside.models import Task
from fireside.models import TaskSchedule
from fireside.models import TaskPriority
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
    task = Task.objects.get(name="Repair Ship")
    assert task.name == "Repair Ship"

    # test create task
    task_schedule = TaskSchedule.objects.create(
        task=task,
        cron="* * * * *",
        repeat=2,
        priority=TaskPriority.LOW,
        inputs={
            "args": str(bsg.uid),
            "kwargs": {},
        },
    )
    assert TaskSchedule.objects.get(task=task).task == task

    # test queue
    assert task_schedule.get_queue().name == TaskPriority.LOW

    # test job in scheduler
    scheduler = get_scheduler()
    assert task_schedule.job_id in scheduler

    # test job
    assert task_schedule.get_job().id == task_schedule.job_id
