import json

from django.utils import timezone

from fireside.protocols import PError, PMetric
from fireside.protocols.defs import TaskTree


def test_protocols():

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


def test_base_models():

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
        "children": [
            {"task_uid": "task2", "children": []},
            {
                "task_uid": "task3",
                "children": [
                    {"task_uid": "task4", "children": []},
                    {"task_uid": "task5", "children": []},
                ],
            },
        ],
    }
