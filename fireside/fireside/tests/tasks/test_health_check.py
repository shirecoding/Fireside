from datetime import timedelta
from operator import attrgetter

from django.utils import timezone
from toolz import groupby


def test_health_check(db):
    from fireside.tasks.health_check import (
        health_check,  # need to import here as it requires db connection
    )

    # test function
    pdict = health_check()
    services = groupby(attrgetter("service"), pdict.services)
    assert services["db"][0].status == "up"
    assert services["db"][0].last_updated > timezone.now() - timedelta(seconds=1)
