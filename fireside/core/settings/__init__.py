import os

_env = os.environ.get("ENVIRONMENT", "development")

if _env == "production":
    from .production import *
elif _env == "test":
    from .test import *
else:
    from .development import *
