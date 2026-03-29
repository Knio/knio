import urllib.parse
import collections

import pathlib
import re

URL_REGEX = (r'^('
  r'((?P<protocol>\w+)://)?'
  r'(?P<host>[^\\/\\\\?]+)?'
  # TODO add ports
  r'(?P<path>[^?]+)?'
  r'(\?(?P<args>[^#]*))?'
  r'(#(?P<anchor>.+))?'
  r')$'
)


FORM_URLENCODING_REGEX = (
  r'^('
  r'(?P<var>[^=]+=[^&]*(&[^=]+=[^&]*)*)?'
  r')$'
)


class url(object):
  __slots__ = [
    'protocol',
    'host',
    'path',
    'args',
    'anchor',
    'trailing_slash',
  ]
  def __init__(self, data=None, **kwargs):
    self.protocol = None
    self.host = None
    self.path = '/'
    self.args = {}
    self.anchor = None
    self.trailing_slash = False
    if data is None:
      pass
    elif isinstance(data, str):
      m = re.match(URL_REGEX, data)
      if m:
        self.update(**dict(i for i in m.groupdict().items() if i[1]))
    elif isinstance(data, url):
      self.protocol = data.protocol
      self.host = data.host
      self.path = data.path
      self.args = data.args
      self.anchor = data.anchor
      self.trailing_slash = data.trailing_slash
      if isinstance(self.args, dict):
        self.args = dict(self.args)
    else:
      raise ValueError

    self.update(**kwargs)

    a = self.parse_arguments(self.args)
    if a:
      self.args = a

    if isinstance(self.path, str):
      decoded = urllib.parse.unquote_plus(self.path)
      self.trailing_slash = decoded != '/' and decoded.endswith('/')
      self.path = pathlib.PurePosixPath(decoded)

  def update(self, **args):
    for k, v in args.items():
      setattr(self, k, v)
    return self

  def update_args(self, *a, **kw):
    self.args.update(*a, **kw)
    return self

  @staticmethod
  def parse_arguments(data):
    if not isinstance(data, str):
      return None
    match = re.match(FORM_URLENCODING_REGEX, data)
    if not match:
      return None
    argstring = match.group('var')
    if not argstring:
      return None

    args = collections.defaultdict(list)
    for j in argstring.split('&'):
      k, x = j.split('=', 1)
      x = urllib.parse.unquote_plus(x)
      args[k].append(x)

    argsf = {}
    for k, v in args.items():
      if len(v) == 1:
        argsf[k] = v[0]
      else:
        argsf[k] = v

    return argsf

  def get_arg(self, arg, default=None):
    return self.args and self.args.get(arg, default)

  def get_args(self, arg):
    if not isinstance(self.args, dict):
      return None
    v = self.args.get(arg, [])
    if not isinstance(v, (list, tuple)):
      return [v]
    return v

  __getitem__ = get_arg

  def __setitem__(self, arg, val):
    if not isinstance(self.args, dict):
      raise ValueError('url arguments are not form encoded')
    self.args[arg] = val

  def __str__(self):
    ret = []
    host = self.host
    if self.protocol is not None:
      ret.append(f'{self.protocol}://')
      host = host or ''

    if host is not None:
      ret.append(host)

    if self.path is not None:
      ret.append(str(self.path))

    if len(self.path.parts) and self.trailing_slash:
      ret.append('/')

    if self.args is None:
      pass
    elif isinstance(self.args, str):
      ret.append(f'?{self.args}')
    elif isinstance(self.args, dict):
      a = []
      for k, v in sorted(self.args.items()):
        if isinstance(v, (str, int, float)):
          v = urllib.parse.quote_plus(str(v))
          a.append(f'{k!s}={v}')
        elif isinstance(v, (list, tuple)):
          for j in v:
            j = urllib.parse.quote_plus(str(j))
            a.append(f'{k!s}={j}')
        else:
          raise ValueError(f'don\'t know how to encode {v!r} (type: {type(v)})')
      if a:
        ret.append('?' + '&'.join(a))
    else:
      ret.append('?' + str(self.args))

    if self.anchor is not None:
      ret.append('#' + str(self.anchor))

    return ''.join(ret)

  def __repr__(self):
    attrs = [f'{k}={getattr(self, k)!r}' for k in type(self).__slots__]
    return f'<{type(self)} {" ".join(attrs)}>'
