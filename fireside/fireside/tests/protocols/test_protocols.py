import json

from django.utils import timezone

from fireside.protocols import PError, PMetric, PTaskChain
from fireside.protocols.defs import TaskTree
from fireside.utils import import_path_to_function


def validate_protocol(protocol):

    klass = import_path_to_function(protocol.klass)

    # test serialization
    assert klass.parse_raw(protocol.json()) == protocol

    # test as_pdict
    assert protocol.as_pdict() == {protocol.protocol: protocol}

    # test as_pdict jsonify
    assert protocol.as_pdict(jsonify=True) == {protocol.protocol: protocol.dict()}


def test_metrics():

    pmetric = PMetric(
        started_on=timezone.now(),
        error=PError(type="IndexError", value="tuple index out of range"),
    )
    validate_protocol(pmetric)


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
    validate_protocol(ptaskchain)
