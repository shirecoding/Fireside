from django.utils import timezone

from fireside.protocols import PError, PMetric


def test_protocols():

    pmetric = PMetric(
        started_on=timezone.now(),
        error=PError(type="IndexError", value="tuple index out of range"),
    )

    # test serialization
    assert PMetric.parse_raw(pmetric.json()) == pmetric

    # test as_kwargs
    assert pmetric.as_kwargs() == {"pmetric": pmetric}

    # test as_kwargs jsonify
    assert pmetric.as_kwargs(jsonify=True) == {"pmetric": pmetric.json()}
