__all__ = ["api", "misc_router"]

from ninja import NinjaAPI, Router

# from ninja.security import django_auth  # default django cookie based authentication

# Warning: It is not secure to use API's with cookie-based authentication without csrf
# api = NinjaAPI(urls_namespace="fireside", auth=django_auth, csrf=True)
api = NinjaAPI(urls_namespace="fireside")

# routers
misc_router = Router()

# add routers
api.add_router("/misc/", misc_router)
