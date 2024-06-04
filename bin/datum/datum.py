import struct

class FieldDescriptor:
  def __init__(self, name=None, expr=None, **kwargs):
    self.name = name
    self.expr = expr


  def __repr__(self):
    l = ', '.join(
      list(map(repr, self.args)) +
      list(f'{k}={v!r}' for k, v in self.kwargs.items())
    )
    return f'<F {l}>'


class DatumMeta(type):
  def __new__(cls, name, bases, dct):
    print((cls, name, bases, dct))

    A = dct.get('__annotations__', {})
    T = super().__new__(cls, name, bases, dct)
    A = T.__annotations__
    print((T, A))
    return T


class DatumBase:
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

  def size(self):
    raise NotImplementedError


class Datum(DatumBase, metaclass=DatumMeta):
  def __init__(self, *args, **kwargs):
    T = type(self)
    A = T.__annotations__
    self._items = {}
    self._size = 0
    args = list(args)
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
      self._size += item.size()
    # raise ValueError(self, A)

  def __getattr__(self, k):
    try:
      return self._items[k].value()
    except KeyError:
      raise AttributeError(k)

  def __repr__(self):
    x = '<'
    x += type(self).__name__
    x += ' '
    x += ' '.join(f'{k}={v}' for k,v in self.items())
    x += '>'
    return x

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
      v.deserialize(buf[i:i+s])
      i += s
    return self


def datum_struct(fmt):
  s = struct.Struct(fmt)
  class DatumStruct(DatumBase):
    def __init__(self, v):
      # TODO: input validation
      self.v = v

    def serialize(self):
      return s.pack(self.v)

    def deserialize(self, buf):
      assert len(buf) == s.size
      self.v, = s.unpack(buf)
      return self

    def value(self):
      return self.v

    def size(self):
      return s.size

  return DatumStruct

i8  = int8  = datum_struct('!b')
i16 = int16 = datum_struct('!h')
i32 = int32 = datum_struct('!i')
i64 = int64 = datum_struct('!q')

u8  = uint8  = datum_struct('!B')
u16 = uint16 = datum_struct('!H')
u32 = uint32 = datum_struct('!I')
u64 = uint64 = datum_struct('!Q')

# TODO: make u128 types

# TODO: make crc type that validates itself

# TODO: make start/header type that validates itself

# TODO: make size type that validates itself

