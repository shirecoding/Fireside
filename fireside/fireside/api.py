__all__ = ["api"]

from ninja import NinjaAPI

from .utils.widgets.api import router as widget_router

api = NinjaAPI(urls_namespace="fireside")

# add routers
api.add_router("/widget/", widget_router)
