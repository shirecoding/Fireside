from datetime import datetime

from deepdiff import DeepDiff

from fireside.models import Task
from fireside.utils import function_to_import_path
from fireside.utils.task import get_task_result


def test_health_check(db):
    from fireside.tasks.health_check import (
        health_check,  # need to import here as it requires db connection
    )

    # test function call
    hc = health_check()
    assert not DeepDiff(
        [s.dict() for s in hc["services"]],
        [{"service": "db", "status": "up", "last_updated": datetime.now()}],
        truncate_datetime="minute",
    )

    # test task
    health_check_task = Task.objects.create(
        name="HealthCheck",
        description="HealthCheck Task",
        fpath=function_to_import_path(health_check),
    )

    job = health_check_task.enqueue()
    hc = get_task_result(job)

    assert not DeepDiff(
        [s.dict() for s in hc["services"]],
        [{"service": "db", "status": "up", "last_updated": datetime.now()}],
        truncate_datetime="minute",
    )
