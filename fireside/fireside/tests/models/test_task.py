from django_rq import get_scheduler

from fireside.models import Task, TaskPriority
from fireside.utils.task import task as task_decorator


def test_task_decorator(db):
    @task_decorator(name="Task From Decorator", description="Task From Decorator")
    def healthcheck(event):
        pass

    task = Task.objects.get(name="Task From Decorator")
    assert task.name == "Task From Decorator"
    assert task.description == "Task From Decorator"


def test_task_schedule(task_schedule):

    # test queue
    assert task_schedule.get_queue().name == TaskPriority.LOW

    # test job in scheduler
    scheduler = get_scheduler()
    assert task_schedule.job_id in scheduler

    # test job
    assert task_schedule.get_job().id == task_schedule.job_id


def test_task_preset(task_preset):
    pass
