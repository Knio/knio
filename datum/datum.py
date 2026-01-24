import logging
import functools
import struct
import sys


try:
  import annotationlib
except ImportError:
  annotationlib = None

LOG = logging.getLogger(__name__)


class DatumMeta(type):
  def __new__(cls, name, bases, dct):
    if annotationlib:
      annotate = annotationlib.get_annotate_from_class_namespace(dct)
      if annotate:
        annotations = annotationlib.call_annotate_function(
          annotate, format=annotationlib.Format.VALUE
        )
        A = annotations
      else:
        A = {}
    else:
      A = dct.pop('__annotations__', {})

    D = {}
    for k, v in A.items():
      if isinstance(v, functools.partial):
        A[k] = v()
      # remove default values from class attributes
      if clsattr := dct.get(k):
        if not callable(clsattr):
          D[k] = clsattr
          dct.pop(k)

    FA = {}
    FD = {}
    for bb in bases:
      if an := getattr(bb, '_attributes', None):
        FA.update(an)
        FD.update(getattr(bb, '_defaults'))
    FA.update(A)
    FD.update(D)

    dct['_attributes'] = FA
    dct['_defaults'] = FD

    szs = [getattr(c, '_size', False) for c in A.values()]
    if all(szs):
      dct['_size'] = sum(szs)
    T = super().__new__(cls, name, bases, dct)
    return T


class DatumBase:
  def __init__(self, *a, **kw):
    self.set_value(*a, **kw)

  def pre_serialize(self, parent=None):
    pass

  def serialize(self):
    pass

  def deserialize_into(self, buf, parent=None):
    raise NotImplementedError()

  def post_deserialize(self, parent=None):
    pass

  @classmethod
  def deserialize_new(cls, buf, parent=None):
    d = cls()
    n = d.deserialize_into(buf)
    assert n <= len(buf), f'need {n} bytes, got {len(buf)}'
    return d, buf[n:]

  def value(self):
    return self

  def set_value(self, *a, **kw):
    raise NotImplementedError()

  def size(self):
    raise NotImplementedError()


class Datum(DatumBase, metaclass=DatumMeta):
  __slots__ = ['_items']
  def __init__(self, *args, **kwargs):
    object.__setattr__(self, '_items', {}) # TODO should i just use __dict__?
    # TODO compute these in the metaclass - so we can have static size
    T = type(self)
    A = T._attributes
    D = T._defaults
    args = list(args)
    for k, v in A.items():
      if args:
        pv = args.pop(0)
        if k in kwargs:
          raise ValueError(f'{k} provided twice')
        if type(pv) is v:
          item = pv
        else:
          item = v(pv)
      else:
        if k in kwargs:
          item = v(kwargs.pop(k))
        elif k in D:
          item = v(D[k])
        else:
          item = v()
      self._items[k] = item

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
    if (v := self.value()) != self:
      return repr(v)
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
    return self.pre_serialize()

  def pre_serialize(self):
    sz = 0
    for v in self._items.values():
      v.pre_serialize(self)
      sz += v.size()
    return sz

  def serialize(self):
    self.pre_serialize()
    return b''.join(v.serialize() for v in self._items.values())

  def deserialize_into(self, buf, parent=None):
    i = 0
    for v in self._items.values():
      s = v.deserialize_into(buf[i:], self)
      i += s
    for v in self._items.values():
      v.post_deserialize(self)
    return i


class DatumStruct(DatumBase):
  def set_value(self, v=0):
    # TODO: input validation
    self.v = v

  def serialize(self):
    return self._struct.pack(self.v)

  def deserialize_into(self, buf, parent=None):
    sz = self.size()
    assert len(buf) >= sz
    self.v, = self._struct.unpack(bytes(buf[:sz]))
    return sz

  def value(self):
    return self.v

  def size(self):
    return self._struct.size

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

  def deserialize_into(self, buf, parent=None):
    sz = self.size()
    assert len(buf) >= sz
    self.v = int.from_bytes(buf[:sz],
      byteorder=self._byteorder,
      signed=self._signed)
    return sz

  def value(self):
    return self.v

  @classmethod
  def size(cls):
    return cls._size

class BigIntEnumDatum(BigIntDatum):
  def value(self):
    return self._enum(self.v)



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
u128= functools.partial(datum_bigint, size=16, signed=False)
fp32= functools.partial(datum_struct, 'f')

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

u16le = functools.partial(u16, endian='little')
u32le = functools.partial(u16, endian='little')


class Array(DatumBase, list):
  # TODO: alignment/padding

  def __init__(self, *a, **kw):
    list.__init__(self, *a, **kw)

  def size(self):
    sz = self._child_type._size
    return sz * len(self)

  def _get_length_item(self, parent):
    # TODO other options for size
    return parent._items[self._length]

  def get_length(self, parent):
    if isinstance(self._length, int):
      return self._length
    n = self._get_length_item(parent).value() + self._bias
    return n

  def pre_serialize(self, parent):
    if isinstance(self._length, int):
      return
    self._get_length_item(parent).set_value(len(self) - self._bias)

  def serialize(self):
    return b''.join(v.serialize() for v in self)

  def deserialize_into(self, buf, parent):
    n = self.get_length(parent)
    cs = self._child_type._size
    N = n * cs
    if N > len(buf):
      raise ValueError(f'need at least {N} bytes, got {len(buf)}')
    self[:] = []
    for i in range(0, N, cs):
      c, _ex = self._child_type.deserialize_new(buf[i:i+cs])
      assert not _ex
      self.append(c.value())
    return N


def array(child_type=u8(), length=None, bias=0):
  if isinstance(child_type, functools.partial):
    child_type = child_type()
  class FixedArray(Array):
    _child_type = child_type
    _length = length
    _bias = bias
  return FixedArray
# TODO: str/bytes type that coercers this into b''/'' instead of []



# TODO: (oneof type) if field a is X, interpret field b as Y
# TODO: make crc type that sets/validates itself
# TODO: make start/header type that -sets-/validates itself

