# __all = ["task_chain"]

# import logging

# from fireside.protocols import Protocol, PTaskChain, PProtocolDict
# from fireside.utils.task import task
# from fireside.models import Task

# logger = logging.getLogger(__name__)


# @task(name="TaskChain", description="Chain a tree of tasks")
# def task_chain(pprotocoldict: PProtocolDict, ptaskchain: PTaskChain) -> PTaskChain:
#     """
#     PROB: Problem input is a generic protocol, type hints will fail, need to support params not being tied to the protocol name!!!!

#     because preset as_kwargs() is used to jsonify the model and as_kwargs will use the protocol name instead of the function args

#     problem also if tasks take in 2 of the same type of protocols, the keyworc cannot be pmetric1/2


#     the pdict keys are rather the function input keys rather than the pkeys,
#     """

#     # TODO: check that input matches the input of taskchain


#     # for task_tree in ptaskchain.task_chain:
#     #     Task.objects.get(uid=task_tree.task_uid).enqueue()
