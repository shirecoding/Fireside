from .base import *  # noqa

ENVIRONMENT = "test"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Run rq in async mode during test (force it to use test database)
for queue_config in RQ_QUEUES.values():  # noqa
    queue_config["ASYNC"] = False
