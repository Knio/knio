import pytest

import datum

def test_basic():
    class Point(datum.Datum):
        x: datum.int32
        y: datum.int32

    p = Point(14, 37)
    assert p.size() == 8
    p2 = Point.deserialize_new(p.serialize())
    assert p2.x == 14
    assert p2.y == 37
    assert p2.values() == (14, 37)
    assert p2.dict() == {'x':14, 'y':37}
    assert f'{p2}' == '<Point x=14 y=37>'


def test_datum():
    class TestDatum(datum.Datum):
        x: datum.int8
        y: datum.uint32

    d = TestDatum(-1, 1)

    assert d.x == -1
    assert d.y == 1


if __name__ == "__main__":
    exit(pytest.main(['-v']))

