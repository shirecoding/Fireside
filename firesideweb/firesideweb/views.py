# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from django import template
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy("login"))
def index(request):

    context = {}
    context["segment"] = "index"

    # html_template = loader.get_template("index.html")  # django softui index.html
    html_template = loader.get_template("build/index.html")  # react chat index.html

    return HttpResponse(html_template.render(context, request))


@login_required(login_url=reverse_lazy("login"))
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split("/")[-1]
        context["segment"] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template("page-500.html")
        return HttpResponse(html_template.render(context, request))
