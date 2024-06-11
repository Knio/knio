import functools
import struct
import sys


class DatumMeta(type):
  def __new__(cls, name, bases, dct):
    print((cls, name, bases, dct))

    A = dct.get('__annotations__', {})
    for k, v in A.items():
      if isinstance(v, functools.partial):
        A[k] = v()
    T = super().__new__(cls, name, bases, dct)
    return T


class DatumBase:
  def __init__(self, *a, **kw):
    self.set_value(*a, **kw)

  def serialize(self):
    pass

  def deserialize_into(self, buf):
    raise NotImplementedError()

  @classmethod
  def deserialize_new(cls, buf):
    n = cls()
    n.deserialize_into(buf)
    return n

  def value(self):
    return self

  def set_value(self):
    raise NotImplementedError

  def size(self):
    raise NotImplementedError


class Datum(DatumBase, metaclass=DatumMeta):
  __slots__ = ['_size', '_items']
  def __init__(self, *args, **kwargs):
    T = type(self)
    A = T.__annotations__
    # self._items = {}
    object.__setattr__(self, '_items', {})
    args = list(args)
    size = 0
    for k, v in A.items():
      if args:
        pv = args.pop(0)
        if k in kwargs:
          raise ValueError(f'{k} provided twice')
      else:
        pv = kwargs.pop(k, None)
        if not pv:
          # get default value
          pv = getattr(T, k, None)

      item = v(pv)
      self._items[k] = item
      size += item.size()
    object.__setattr__(self, '_size', size)

  def __getattr__(self, k):
    try:
      return self._items[k].value()
    except KeyError:
      raise AttributeError(k)

  def __setattr__(self, k, v):
    if k in self._items:
      self._items[k].set_value(v)
    else:
      raise AttributeError(k)
    return super().__setattr__(k, v)

  def __repr__(self):
    return ''.join((
      '<', type(self).__name__,
      ' ',
      ' '.join(f'{k}={v!r}' for k,v in self.items()),
      '>',
    ))

  def values(self):
    return tuple(v.value() for v in self._items.values())

  def items(self):
    return tuple((k, v.value()) for k, v in self._items.items())

  def dict(self):
    return {k: v.value() for k, v in self._items.items()}

  def size(self):
    return self._size

  def serialize(self):
    return b''.join(v.serialize() for v in self._items.values())

  def deserialize_into(self, buf):
    i = 0
    for v in self._items.values():
      s = v.size()
      v.deserialize_into(buf[i:i+s])
      i += s
    return self


class DatumStruct(DatumBase):
  def set_value(self, v=0):
    # TODO: input validation
    self.v = v

  def serialize(self):
    return self._struct.pack(self.v)

  def deserialize_into(self, buf):
    assert len(buf) == self._struct.size
    self.v, = self._struct.unpack(buf)
    return self

  def value(self):
    return self.v

  def size(self):
    return self._struct.size


class BigIntDatum(DatumBase):
  __slots__ = ['v']
  def set_value(self, v=0):
    # TODO: input validation
    self.v = v

  def serialize(self):
    return self.v.to_bytes(
      length=self._size,
      byteorder=self._byteorder,
      signed=self._signed
    )

  def deserialize_into(self, buf):
    assert len(buf) == self._size
    self.v = int.from_bytes(buf,
      byteorder=self._byteorder,
      signed=self._signed)
    return self

  def value(self):
    return self.v

  def size(self):
    return self._size

class BigIntEnumDatum(BigIntDatum):
  def value(self):
    return self._enum(self.v)


def datum_struct(fmt, endian='network'):
  e = dict(
    network='!',
    native='@',
    big='>',
    little='<'
  )[endian]
  class DS(DatumStruct):
    _struct = struct.Struct(f'{e}{fmt}')
  return DS

def datum_bigint(size=1, endian='big', signed=True, enum=None):
  if endian == 'native':
    endian = sys.byteorder
  if endian == 'network':
    endian = 'big'
    # TODO just use type() and set the name etc
  base = BigIntDatum
  if enum:
    base = BigIntEnumDatum
  class BI(base):
    _size = size
    _byteorder = endian
    _signed = signed
    _enum = enum
  return BI


i8  = functools.partial(datum_struct, 'b')
u32 = functools.partial(datum_struct, 'I')
i32 = functools.partial(datum_struct, 'i')
u128 =functools.partial(datum_bigint, size=16, signed=False)

# u8  = uint8  = datum_struct('B')
# i8  = int8  = datum_struct('b')
# i16 = int16 = datum_struct('h')
# i32 = int32 = datum_struct('i')
# i64 = int64 = datum_struct('q')

u8  = functools.partial(datum_bigint, size=1, signed=False)
u16 = functools.partial(datum_bigint, size=2, signed=False)
u32 = functools.partial(datum_bigint, size=4, signed=False)
u64 = functools.partial(datum_bigint, size=8, signed=False)

i8  = functools.partial(datum_bigint, size=1)
i16 = functools.partial(datum_bigint, size=2)
i32 = functools.partial(datum_bigint, size=4)
i64 = functools.partial(datum_bigint, size=8)


# TODO: if feild a is X, interpret feild b as Y

# TODO: make crc type that validates itself

# TODO: make start/header type that validates itself

# TODO: make size type that validates itself

