import pytest
from fireside.models import Task
from fireside.models import TaskSchedule
from fireside.models import TaskPriority
from fireside.models import ActivatableModel
from django.utils import timezone
from datetime import timedelta
from fireside.utils import function_to_import_path


def dummy_task(*args, **kwargs):
    pass


@pytest.fixture
def task_schedule(db) -> TaskSchedule:

    assert issubclass(TaskSchedule, ActivatableModel)

    # create Task
    task = Task.objects.create(
        name="Dummy Task",
        description="Dummy Task",
        fpath=function_to_import_path(dummy_task),
    )

    # create TaskSchedule
    task_schedule = TaskSchedule.objects.create(
        task=task,
        cron="* * * * *",
        repeat=2,
        priority=TaskPriority.LOW,
        inputs={},
    )
    assert TaskSchedule.objects.get(task=task).task == task

    return task_schedule


def test_activatable_model(task_schedule):

    now = timezone.now()

    # test default is_active
    assert task_schedule.activate_on == task_schedule.deactivate_on == None
    assert task_schedule.is_active == True

    # test deactivate
    task_schedule.deactivate()
    assert task_schedule.is_active == False

    # test activate
    task_schedule.activate()
    assert task_schedule.activate_on == task_schedule.deactivate_on == None
    assert task_schedule.is_active == True

    # test deactivate_on
    task_schedule.deactivate_on = now - timedelta(seconds=60)
    task_schedule.save()
    assert task_schedule.is_active == False

    # test activate_on
    task_schedule.activate()
    assert task_schedule.activate_on == task_schedule.deactivate_on == None
    task_schedule.activate_on = now - timedelta(seconds=60)
    task_schedule.save()
    assert task_schedule.is_active == True

    # test deactivate_on & activate_on
    task_schedule.activate()
    assert task_schedule.activate_on == task_schedule.deactivate_on == None
    task_schedule.activate_on = now - timedelta(seconds=60)
    task_schedule.deactivate_on = now + timedelta(seconds=60)
    task_schedule.save()
    assert task_schedule.is_active == True

    task_schedule.activate_on = now + timedelta(seconds=60)
    task_schedule.deactivate_on = now + timedelta(seconds=60)
    task_schedule.save()
    assert task_schedule.is_active == False

    task_schedule.activate_on = now - timedelta(seconds=60)
    task_schedule.deactivate_on = now - timedelta(seconds=60)
    task_schedule.save()
    assert task_schedule.is_active == False
