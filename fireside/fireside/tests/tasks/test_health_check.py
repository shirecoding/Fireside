from datetime import datetime

from deepdiff import DeepDiff

from fireside.models import Task
from fireside.protocols import as_serialized_pdict
from fireside.utils import function_to_import_path
from fireside.utils.task import get_task_result


def test_health_check(db):
    from fireside.tasks.health_check import (
        health_check,  # need to import here as it requires db connection
    )

    # test function
    pdict = health_check()
    assert not DeepDiff(
        as_serialized_pdict(pdict),
        {
            "phealthcheck": {
                "klass": "fireside.tasks.health_check.PHealthCheck",
                "protocol": "phealthcheck",
                "services": [
                    {"last_updated": datetime.now(), "service": "db", "status": "up"}
                ],
            }
        },
        truncate_datetime="minute",
    )

    # test task
    health_check_task = Task.objects.create(
        name="HealthCheck",
        description="HealthCheck Task",
        fpath=function_to_import_path(health_check),
    )

    job = health_check_task.enqueue()
    pdict = get_task_result(job)

    assert not DeepDiff(
        as_serialized_pdict(pdict),
        {
            "phealthcheck": {
                "klass": "fireside.tasks.health_check.PHealthCheck",
                "protocol": "phealthcheck",
                "services": [
                    {"last_updated": datetime.now(), "service": "db", "status": "up"}
                ],
            }
        },
        truncate_datetime="minute",
    )
