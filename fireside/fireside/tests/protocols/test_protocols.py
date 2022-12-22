import json

from django.utils import timezone

from fireside.protocols import PError, PMetric, PTaskChain
from fireside.protocols.defs import TaskTree


def test_metrics():

    pmetric = PMetric(
        started_on=timezone.now(),
        error=PError(type="IndexError", value="tuple index out of range"),
    )

    # test serialization
    assert PMetric.parse_raw(pmetric.json()) == pmetric

    # test as_kwargs
    assert pmetric.as_kwargs() == {"pmetric": pmetric}

    # test as_kwargs jsonify
    assert pmetric.as_kwargs(jsonify=True) == {"pmetric": pmetric.json()}


def test_task():

    # test TaskTree
    ttree = TaskTree(
        task_uid="task1",
        children=[
            TaskTree(task_uid="task2"),
            TaskTree(
                task_uid="task3",
                children=[
                    TaskTree(task_uid="task4"),
                    TaskTree(task_uid="task5"),
                ],
            ),
        ],
    )

    assert json.loads(ttree.json()) == {
        "task_uid": "task1",
        "job_id": None,
        "children": [
            {"task_uid": "task2", "job_id": None, "children": []},
            {
                "task_uid": "task3",
                "job_id": None,
                "children": [
                    {"task_uid": "task4", "job_id": None, "children": []},
                    {"task_uid": "task5", "job_id": None, "children": []},
                ],
            },
        ],
    }

    # test PTaskChain
    ptaskchain = PTaskChain(task_chain=[ttree])

    # test serialization
    assert PTaskChain.parse_raw(ptaskchain.json()) == ptaskchain

    # test as_kwargs
    assert ptaskchain.as_kwargs() == {"ptaskchain": ptaskchain}

    # test as_kwargs jsonify
    assert ptaskchain.as_kwargs(jsonify=True) == {"ptaskchain": ptaskchain.json()}
