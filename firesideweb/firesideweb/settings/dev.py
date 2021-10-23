from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

if env("PROXY_DB").lower() == "true":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }

try:
    pass
except ImportError:
    pass
