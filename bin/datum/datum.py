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
    def to_bytes(self):
      pass

    T = super().__new__(cls, name, bases, dct)
    A = T.__annotations__
    print((T, A))
    return T

  @staticmethod
  def foo(A):
    return 'bar'


class DatumBase:
  def serialize(self):
    pass

  def deserialize(bytes):
    pass

  def value(self):
    return self

  def size(self):
    raise NotImplemented


class Datum(DatumBase, metaclass=DatumMeta):
  def __init__(self, *args, **kwargs):
    T = type(self)
    A = T.__annotations__
    self._items = {}
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
      self._items[k] = v(pv)
    # raise ValueError(self, A)

  def __getattr__(self, k):
    return self._items[k].value()

  def serialize(self):
    return b''.join(v.serialize() for v in self._items.values())

  def deserialize(self, buffer):
    i = 0
    for v in self._items.values():
      s = v.size()
      v.deserialize(buffer[i:i+s])
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

    def deserialize(self, buffer):
      assert len(buffer) == s.size
      self.v, = s.unpack(buffer)
      return self

    def value(self):
      return self.v

    def size(self):
      return s.size

  return DatumStruct

int8  = datum_struct('!b')
int16 = datum_struct('!h')
int32 = datum_struct('!i')
int64 = datum_struct('!q')

uint8  = datum_struct('!B')
uint16 = datum_struct('!H')
uint32 = datum_struct('!I')
uint64 = datum_struct('!Q')

