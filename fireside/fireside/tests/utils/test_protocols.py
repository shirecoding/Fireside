from django.utils import timezone

from fireside.utils import PError, PMetric


def test_protocols():

    pmetric = PMetric(
        started_on=timezone.now(),
        error=PError(type="IndexError", value="tuple index out of range"),
    )

    # test ClassVar
    assert PMetric.protocol == pmetric.protocol

    # test serialization
    assert PMetric.parse_raw(pmetric.json()) == pmetric

    # test as kwargs
    assert pmetric.as_kwargs() == {PMetric.protocol: pmetric}
