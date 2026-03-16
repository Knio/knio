import pytest

import datum


# pyright: reportInvalidTypeForm=false


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
      x: datum.i8()
      y: datum.u32()

  d = TestDatum(-1, 1)
  assert d.x == -1
  assert d.y == 1
  d.x = 2
  assert d.x == 2


def test_bigint():
  i = datum.u16()(5)
  assert i.serialize() == b'\x00\x05'
  i.set_value(4)
  assert i.serialize() == b'\x00\x04'
  buf = bytearray(4)
  assert i.serialize_into(buf, 2) == 2
  assert bytes(buf) == b'\x00\x00\x00\x04'


def test_enum():
  # TODO
  pass

def test_serialize():
  class Point(datum.Datum):
      x: datum.i32()
      y: datum.i32()

  p = Point(14, 37)
  assert p.size() == 8
  b = p.serialize()
  assert b == b'\x00\x00\x00\x0e\x00\x00\x00\x25'
  p2, _ex = Point.deserialize_new(b)
  assert p2.x == 14
  assert p2.y == 37
  assert p2.values() == (14, 37)
  assert p2.dict() == {'x':14, 'y':37}
  assert f'{p2}' == '<Point x=14 y=37>'
  p2.y = 38
  with pytest.raises(AttributeError):
    p2.z = 3
  p3, _ex = Point.deserialize_new(p2.serialize())
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
  assert f'{t}' == "<C a=3 b='foo' c=2.71>"


def test_defaults():
  class A(datum.Datum):
    x: int = 4
  class B(A):
    x: int = 5

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
    assert cls.deserialize_new(buf)[0].value() == v

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
    x: datum.i32()
    y: datum.i32

  a = Point(1, 2)
  assert a.x == 1
  assert a.y == 2

  class Triangle(datum.Datum):
    a: Point
    b: Point
    c: Point

  t = Triangle(Point(1, 2), Point(3, 4), Point(5, 6))
  assert t.b.x == 3
  assert t.b.y == 4


  assert repr(t) == "<Triangle a=<Point x=1 y=2> b=<Point x=3 y=4> c=<Point x=5 y=6>>"


def test_array():
  class Point(datum.Datum):
    x: datum.i16()
    y: datum.i16

  # TODO test fixed-length arrays

  class PA(datum.Datum):
    n: datum.u8
    points: datum.array(Point, length='n', bias=-1)

  p1 = Point(1,2)
  p2 = Point(3,4)
  pa = PA(0, [p1, p2])
  assert repr(pa) == "<PA n=0 points=[<Point x=1 y=2>, <Point x=3 y=4>]>"

  pa.pre_serialize()
  assert repr(pa) == "<PA n=3 points=[<Point x=1 y=2>, <Point x=3 y=4>]>"

  b = pa.serialize()
  assert b == b'\x03\x00\x01\x00\x02\x00\x03\x00\x04'

  pa, _ex = PA.deserialize_new(b)
  assert pa.n == 3
  assert len(pa.points) == 2
  assert pa.points[0].x == 1
  assert pa.points[0].y == 2
  assert pa.points[1].x == 3
  assert pa.points[1].y == 4


if __name__ == "__main__":
  exit(pytest.main(['-vv']))

