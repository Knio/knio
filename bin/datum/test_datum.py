import pytest

import datum

def test_datum():
    class TestDatum(datum.Datum):
        x: datum.int8
        y: datum.uint32

    d = TestDatum(-1, 1)

    assert d.x == -1
    assert d.y == 1
    b = d.serialize()
    assert b == b'\xff\0\0\0\x01'

    c = TestDatum().deserialize(b)
    assert c.x == -1
    assert c.y == 1

if __name__ == "__main__":
    exit(pytest.main(['-v']))

