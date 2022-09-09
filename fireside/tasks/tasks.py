from tasks.utils import register_task

# TODO:
#
#   - Create task to read tasks, push job to queue
#


@register_task(name="Dummy Task", description="This is a dummy task")
def dummy_task():
    pass
