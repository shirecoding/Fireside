from .base import *
from google.oauth2 import service_account
import json
from base64 import b64decode

DEBUG = False

ALLOWED_HOSTS = [env("HOST")]

#####################################################################################
# Storage
#####################################################################################

GS_PROJECT_ID = env("GS_PROJECT_ID")
GS_MEDIA_BUCKET_NAME = env("GS_MEDIA_BUCKET_NAME")
GS_STATIC_BUCKET_NAME = env("GS_STATIC_BUCKET_NAME")
GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
    json.loads(b64decode(env("APP_ENGINE_SVC_KEY")))
)
GS_BUCKET_NAME = env("GS_MEDIA_BUCKET_NAME")
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
STATICFILES_STORAGE = "crossshare.storages.GoogleCloudStaticFileStorage"

#####################################################################################
# Database
#####################################################################################

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": "5432",
    }
}

try:
    pass
except ImportError:
    pass
