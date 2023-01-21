__all__ = ["api", "misc_router"]

from ninja import NinjaAPI, Router

api = NinjaAPI(urls_namespace="fireside")

# routers
misc_router = Router()

# add routers
api.add_router("/misc/", misc_router)
