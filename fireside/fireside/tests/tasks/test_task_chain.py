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

    assert [r.dict() for r in results] == [
        {
            "children": [
                {
                    "children": [],
                    "job_id": "c4df3893-a086-4e42-8846-2acf09cc527b",
                    "result": {
                        "message": {
                            "text": ".God Yzal Eht Revo Spmuj Xof " "Nworb Kciuq Eht"
                        }
                    },
                    "task_uid": "3b2c4c5f-4146-4db8-a798-4d244daa0c2f",
                }
            ],
            "job_id": "1830f68d-b080-41ea-a0e0-1899c11d1d60",
            "result": {
                "message": {"text": ".god yzal eht revo spmuj xof nworb kciuq " "ehT"}
            },
            "task_uid": "b4a4a554-bfa3-4117-aad3-d5941b7ea4ae",
        },
        {
            "children": [],
            "job_id": "4ed6d6f9-149c-4dee-b5a3-fe43ff83226e",
            "result": {
                "message": {"text": "The Quick Brown Fox Jumps Over The Lazy " "Dog."}
            },
            "task_uid": "3b2c4c5f-4146-4db8-a798-4d244daa0c2f",
        },
    ]

    # # test function
    # pdict = health_check()
    # assert not DeepDiff(
    #     as_serialized_pdict(pdict),
    #     {
    #         "phealthcheck": {
    #             "klass": "fireside.tasks.health_check.PHealthCheck",
    #             "protocol": "phealthcheck",
    #             "services": [
    #                 {"last_updated": datetime.now(), "service": "db", "status": "up"}
    #             ],
    #         }
    #     },
    #     truncate_datetime="minute",
    # )

    # # test task
    # health_check_task = Task.objects.create(
    #     name="HealthCheck",
    #     description="HealthCheck Task",
    #     fpath=function_to_import_path(health_check),
    # )

    # job = health_check_task.enqueue()
    # pdict = get_task_result(job)

    # assert not DeepDiff(
    #     as_serialized_pdict(pdict),
    #     {
    #         "phealthcheck": {
    #             "klass": "fireside.tasks.health_check.PHealthCheck",
    #             "protocol": "phealthcheck",
    #             "services": [
    #                 {"last_updated": datetime.now(), "service": "db", "status": "up"}
    #             ],
    #         }
    #     },
    #     truncate_datetime="minute",
    # )
