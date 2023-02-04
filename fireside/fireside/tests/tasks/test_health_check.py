from datetime import datetime

from deepdiff import DeepDiff
from django.utils import timezone

from fireside.models.task import Task
from fireside.utils import function_to_import_path
from fireside.utils.task import get_task_result


def test_health_check(db):
    from fireside.tasks.health_check import (
        health_check,  # need to import here as it requires db connection
    )

    # test function call
    hc = health_check()
    hc["services"][0]["last_updated"] = datetime.fromisoformat(
        hc["services"][0]["last_updated"]
    )

    assert not DeepDiff(
        hc["services"],
        [{"service": "db", "status": "up", "last_updated": timezone.now()}],
        truncate_datetime="minute",
    )

    # test task
    health_check_task = Task.objects.get(fpath=function_to_import_path(health_check))

    task_log = health_check_task.enqueue()
    hc = get_task_result(task_log)
    hc["services"][0]["last_updated"] = datetime.fromisoformat(
        hc["services"][0]["last_updated"]
    )

    assert not DeepDiff(
        hc["services"],
        [{"service": "db", "status": "up", "last_updated": timezone.now()}],
        truncate_datetime="minute",
    )
