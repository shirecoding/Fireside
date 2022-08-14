import os

if os.environ.get("ENVIRONMENT") == "production":
    from .production import *
elif os.environ.get("ENVIRONMENT") == "test":
    from .test import *
else:
    from .development import *
