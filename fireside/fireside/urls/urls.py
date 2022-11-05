from django.urls import path
from ninja import NinjaAPI

from .utils import router as utils_router

api = NinjaAPI(urls_namespace="fireside")

api.add_router("/utils/", utils_router)

urlpatterns = [
    path("api/", api.urls),
]
