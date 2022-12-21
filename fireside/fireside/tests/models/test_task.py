import logging

from django_rq import get_scheduler

from fireside.models import Task, TaskPriority
from fireside.protocols import ProtocolDict
from fireside.utils.task import task as task_decorator

logger = logging.getLogger(__name__)


def test_task_decorator(db):
    @task_decorator(name="DoNothing", description="This task does nothing")
    def do_nothing(**protocols) -> ProtocolDict:
        return protocols

    task = Task.objects.get(name="DoNothing")
    assert task.name == "DoNothing"
    assert task.description == "This task does nothing"


def test_task_schedule(task_schedule):

    # test queue
    assert task_schedule.get_queue().name == TaskPriority.LOW

    # test job in scheduler
    scheduler = get_scheduler()
    assert task_schedule.job_id in scheduler

    # test job
    assert task_schedule.get_job().id == task_schedule.job_id


def test_task_preset(task_preset, pmessage):

    # test deserialization
    assert task_preset.run() == pmessage.as_kwargs()


def test_task_enqueue(task, pmessage):

    job, obs = task.enqueue(**pmessage.as_kwargs())

    res = obs.run()

    print(f"\n\njob: {job} res {res}\n\n")

    # obs.subscribe(lambda x: logger.debug(f'GOT RESULT {x}'))

    # print(f'\n\njob: {job} obs: {obs}\n\n\n')
