import pytest

import datum

def test_datum():
    class TestDatum(datum.Datum):
        x : float

    d = TestDatum(1)
 
    assert d.x == 1.0
    assert type(d.x) is float

if __name__ == "__main__":
    exit(pytest.main(['-v']))

