
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


class DatumBase(type):
  def __new__(cls, name, bases, dct):
    print((cls, name, bases, dct))

    A = dct.get('__annotations__', {})
    def to_bytes(self):
      pass

    x = super().__new__(cls, name, bases, dct)
    T = x
    A = T.__annotations__
    print((T, A))
    return x

  @staticmethod
  def foo(A):
    pass



class Datum(metaclass=DatumBase):
  def __init__(self, *args, **kwargs):
    T = type(self)
    A = T.__annotations__
    for k, v in A.items():
      if args:
        pv = args.pop(0)
        if k in kwargs:
          raise ValueError(f'{k} provided twice')
        setattr(self, k, pv)
      else:
        pv = kwargs.pop(k, None)
        if not pv:
          # get default value
          pv = getattr(T, k, None)
        setattr(self, k, pv)
    # raise ValueError(self, A)

