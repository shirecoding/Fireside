from tasks.utils import register_task


@register_task(name="Dummy Task", description="This is a dummy task")
def dummy_task():
    pass
