import logging

import markdown as md
from django.http import HttpRequest, HttpResponse
from ninja import Form, Schema

from fireside.api import misc_router

logger = logging.getLogger(__name__)


class Markdown(Schema):
    text: str


@misc_router.post("/render_markdown", url_name="render_markdown")
async def render_markdown(
    request: HttpRequest, response: HttpResponse, markdown: Markdown = Form(...)
) -> HttpResponse:
    return HttpResponse(md.markdown(markdown.text), content_type="text/plain")
