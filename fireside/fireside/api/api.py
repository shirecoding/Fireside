__all__ = ["api", "misc_router"]

from ninja import NinjaAPI, Router

from .security import django_auth_async

api = NinjaAPI(
    urls_namespace="fireside", auth=django_auth_async, csrf=True
)  # Warning: It is not secure to use API's with cookie-based authentication without csrf

# routers
misc_router = Router()

# add routers
api.add_router("/misc/", misc_router)
