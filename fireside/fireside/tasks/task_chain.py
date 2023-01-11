__all = ["task_chain"]

import logging

from fireside.models import Task
from fireside.utils import JSONObject
from fireside.utils.task import TaskTree, get_task_result, task

logger = logging.getLogger(__name__)


def traverse_tree(tree, **kwargs):
    """
    Does a blocking call at each node and passes the result as input to the children.
    When the function returns, the task results are ready to be fetched
    """
    job = Task.objects.get(uid=tree.task_uid).enqueue(**kwargs)
    result_kwargs = get_task_result(job)
    return TaskTree(
        task_uid=tree.task_uid,
        job_id=job.id,
        children=[traverse_tree(t, **result_kwargs) for t in tree.children],
    )


@task(name="TaskChain", description="Chain a tree of tasks")
def task_chain(*, trees: list[TaskTree], initial_kwargs: JSONObject) -> list[TaskTree]:
    return [traverse_tree(t, **initial_kwargs) for t in trees]
