from fireside.utils import remove_falsy, remove_none


def test_remove_none():
    assert remove_none([None, 1, 2, 3]) == [1, 2, 3]
    assert remove_none({None: 1, 2: 3}) == {2: 3}
    assert remove_none({1: None, 2: 3}) == {2: 3}
    assert remove_none({1, 2, None}) == {1, 2}
    assert list(remove_none(x for x in [1, 2, 3, None])) == [1, 2, 3]


def test_remove_falsy():
    assert remove_falsy([False, 1, 2, 3]) == [1, 2, 3]
    assert remove_falsy({False: 1, 2: 3}) == {2: 3}
    assert remove_falsy({1: False, 2: 3}) == {2: 3}
    assert remove_falsy({1, 2, False}) == {1, 2}
    assert list(remove_falsy(x for x in [1, 2, 3, False])) == [1, 2, 3]
