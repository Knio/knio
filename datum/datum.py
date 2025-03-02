import functools
import struct
import sys


class DatumMeta(type):
  def __new__(cls, name, bases, dct):
    A = dct.get('__annotations__', {})
    D = {}
    for k, v in A.items():
      if isinstance(v, functools.partial):
        A[k] = v()
      if clsattr := dct.get(k):
        if not callable(clsattr):
          D[k] = clsattr
          dct.pop(k)

    dct['_defaults'] = D
    # print(f'meta {name} {bases}')
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
    # TODO compute these in the metaclass
    T = type(self)
    A = {}
    D = {}
    num_ann = 0
    for bb in reversed(T.__mro__):
      if an := getattr(bb, '__annotations__', None):
        A.update(an)
        D.update(getattr(bb, '_defaults'))
        num_ann += 1
    # print(T.__mro__)
    # print((A, D))
    object.__setattr__(self, '_items', {}) # TODO should i just use __dict__?
    args = list(args)
    size = 0
    for k, v in A.items():
      if args:
        if num_ann > 1:
          # TODO actually could be ok as long as inheritance chain is linera
          raise ValueError('Must call inherited class with kwargs, not positional args')
        pv = args.pop(0)
        if k in kwargs:
          raise ValueError(f'{k} provided twice')
        item = v(pv)
      else:
        if k in kwargs:
          item = v(kwargs.pop(k))
        elif k in D:
          item = v(D[k])
        else:
          item = v()

      self._items[k] = item
      if size is not None and hasattr(item, 'size'): # TODO typecheck
        size += item.size()
      else:
        size = None
    object.__setattr__(self, '_size', size)

  # TODO replace with property() protocol?
  def __getattr__(self, k):
    item = self._items.get(k)
    if item is None:
      raise AttributeError(k)
    if v := getattr(item, 'value', None): # TODO typecheck on datumbase
      return v()
    return item

  def __setattr__(self, k, v):
    item = self._items.get(k)
    if item is None:
      raise AttributeError(k)
    if s_v := getattr(item, 'set_value', None): # TODO typecheck on datumbase
      s_v(v)
    else:
      super().__setattr__(k, v)

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
    return tuple((k, getattr(self, k)) for k in self._items.keys())

  def dict(self):
    return dict(self.items())

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


# TODO: if field a is X, interpret field b as Y

# TODO: make crc type that sets/validates itself

# TODO: make start/header type that sets/validates itself

# TODO: make size type that sets/validates itself

