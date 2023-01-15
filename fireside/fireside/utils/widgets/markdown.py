import logging

import markdown as md
from django.http import HttpRequest, HttpResponse
from ninja import Form, Schema

from .api import router

logger = logging.getLogger(__name__)


class Markdown(Schema):
    text: str


@router.post("/render_markdown", url_name="render_markdown")
def render_markdown(
    request: HttpRequest, response: HttpResponse, markdown: Markdown = Form(...)
) -> str:
    response["Content-Type"] = "text/html"
    return md.markdown(markdown.text)
