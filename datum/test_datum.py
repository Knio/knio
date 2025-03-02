import pytest

import datum



def test_normal():
  class Test(datum.Datum):
    a: int
    b: str

  t = Test(1, "foo")
  assert t.a == 1
  assert t.b == "foo"
  assert f'{t}' == "<Test a=1 b='foo'>"


def test_datum():
  class TestDatum(datum.Datum):
      x: datum.i8
      y: datum.u32

  d = TestDatum(-1, 1)
  assert d.x == -1
  assert d.y == 1
  d.x = 2
  assert d.x == 2


def test_serialize():
  class Point(datum.Datum):
      x: datum.i32()
      y: datum.i32()

  p = Point(14, 37)
  assert p.size() == 8
  p2 = Point.deserialize_new(p.serialize())
  assert p2.x == 14
  assert p2.y == 37
  assert p2.values() == (14, 37)
  assert p2.dict() == {'x':14, 'y':37}
  assert f'{p2}' == '<Point x=14 y=37>'
  p2.y = 38
  with pytest.raises(AttributeError):
    p2.z = 3
  p3 = Point.deserialize_new(p2.serialize())
  assert f'{p3}' == '<Point x=14 y=38>'



def test_inheritance():
  class A(datum.Datum):
    a: int
  class B(datum.Datum):
    b: str
  class C(A, B):
    c: float

  t = C(a=1, b="foo", c=2.71)
  assert t.a == 1
  assert t.b == "foo"
  assert t.c == 2.71
  t.a = 3
  assert f'{t}' == "<C b='foo' a=3 c=2.71>"


def test_defaults():
  class A(datum.Datum):
    x: int = 4
  class B(A):
    x = 5

  assert B._defaults == {'x': 5}

  assert A().x == 4
  assert B().x == 5

  assert A(1).x == 1
  assert B(1).x == 1


def test_u64():
  f = datum.u128()
  assert f(1).serialize() == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'


def test_basic_types():
  def check(cls, v, buf):
    d = cls(v)
    assert d.serialize() == buf
    assert cls.deserialize_new(buf).value() == v

  check(datum.i8(), 1, b'\1')
  check(datum.i8(), 127, b'\x7f')
  check(datum.i8(), -128, b'\x80')
  check(datum.i8(), -1, b'\xff')
  check(datum.u8(), 255, b'\xff')

  check(datum.u16(), 1, b'\0\1')
  check(datum.u16(), 256, b'\1\0')

  check(datum.u16(endian='network'), 1, b'\0\1')
  check(datum.u16(endian='network'), 256, b'\1\0')

  check(datum.u16(endian='big'), 1, b'\0\1')
  check(datum.u16(endian='big'), 256, b'\1\0')

  check(datum.u16(endian='little'), 1, b'\1\0')
  check(datum.u16(endian='little'), 256, b'\0\1')

  check(datum.u16(endian='native'), 1, b'\1\0')
  check(datum.u16(endian='native'), 256, b'\0\1')


def test_nesting():
  class Point(datum.Datum):
    x: datum.i32
    y: datum.i32

  a = Point(1, 2)

  class Triangle(datum.Datum):
    a: Point
    b: Point
    c: Point

  # t = Triangle(Point(1, 2), Point(3, 4), Point(5, 6))
  assert a.x == 1
  assert a.y == 2
  # assert repr(t) == "<Triangle a=<Point x=1 y=2> b=<Point x=3 y=4> c=<Point x=5 y=6>>"


if __name__ == "__main__":
  exit(pytest.main(['-vv']))

