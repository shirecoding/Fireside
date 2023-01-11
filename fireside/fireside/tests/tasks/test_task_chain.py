import re

from deepdiff import DeepDiff

from fireside.utils.task import TaskTree, get_task_trees_result


def test_task_chain(db, capitalize_message_task, reverse_message_task, text_message):
    from fireside.tasks.task_chain import (
        task_chain,  # need to import here as it requires db connection to create the @task
    )

    trees = [
        TaskTree(
            task_uid=reverse_message_task.uid,
            children=[TaskTree(task_uid=capitalize_message_task.uid)],
        ),
        TaskTree(task_uid=capitalize_message_task.uid),
    ]

    results = get_task_trees_result(
        task_chain(trees=trees, initial_kwargs={"message": text_message})
    )

    assert not DeepDiff(
        [r.dict() for r in results],
        [
            {
                "task_uid": str(reverse_message_task.uid),
                "job_id": "1830f68d-b080-41ea-a0e0-1899c11d1d60",
                "result": {
                    "message": {"text": ".god yzal eht revo spmuj xof nworb kciuq ehT"}
                },
                "children": [
                    {
                        "task_uid": str(capitalize_message_task.uid),
                        "job_id": "c4df3893-a086-4e42-8846-2acf09cc527b",
                        "result": {
                            "message": {
                                "text": ".God Yzal Eht Revo Spmuj Xof Nworb Kciuq Eht"
                            }
                        },
                        "children": [],
                    }
                ],
            },
            {
                "task_uid": str(capitalize_message_task.uid),
                "job_id": "4ed6d6f9-149c-4dee-b5a3-fe43ff83226e",
                "result": {
                    "message": {"text": "The Quick Brown Fox Jumps Over The Lazy Dog."}
                },
                "children": [],
            },
        ],
        exclude_regex_paths=re.compile(r"\['job_id'\]"),
    )
