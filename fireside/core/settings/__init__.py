import os

_env = os.environ.get("ENVIRONMENT", "development").lower()

if _env in ["prod", "production"]:
    from .production import *  # noqa
elif _env in ["test", "testing"]:
    from .test import *  # noqa
else:
    from .development import *  # noqa
