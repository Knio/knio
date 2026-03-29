from collections import defaultdict
import re
import typing
import urllib.parse


def parse_query(string):
  d = {}
  string = string.split('&')
  for pair in filter(None, string):
    is_array = False
    try:
      key, value = map(urllib.parse.unquote_plus, pair.split('=', 1))
      if key.endswith('[]'):
        key   = key[:-2]
        is_array = True
    except ValueError:
      key, value = urllib.parse.unquote_plus(pair), ''
    if is_array:
      if key in d:
        d[key].append(value)
      else:
        d[key] = [value]
    else:
      d[key] = value
  return d


def parse_strval(string):
  if string.startswith('"') and string.endswith('"'):
    return string[1:-1]
  return string


def parse_semi(string):
  d = {}
  for pair in filter(None, string.split('; ')):
    try:
      key, value = pair.split('=',1)
    except ValueError:
      key, value = '', pair
    d[parse_strval(key)] = parse_strval(value)
  return d


def parse_multipart(content_type, data):
  '''
  boggles the fucking mind that this is not in the stdlib
  '''
  multipart = defaultdict(list)
  # TODO use memoryview

  content_type = parse_semi(content_type)
  boundary     = ('--' + content_type['boundary']).encode('utf-8')

  string = data
  if not string.startswith(boundary):
    raise ValueError('form-data boundary does not match')

  class part(typing.NamedTuple):
    headers: dict
    disposition: dict
    name: str
    data: bytes

  def make_part(string):
    headers = {}
    while True:
      n = string.find(b'\r\n')
      if n == -1:
        raise ValueError('Unexpected EOF while parsing form parts.')
      if n == 0:
        string = string[2:-2]
        break
      header, value = string[:n].split(b': ', 1)
      headers[header.decode('utf-8')] = value.decode('utf-8')
      string = string[n+2:]

    data        = string
    disposition = parse_semi(headers['Content-Disposition'])
    name        = disposition.pop('name')
    return part(headers, disposition, name, data)

  string = data[len(boundary + b'\r\n'):]

  while True:
    n = string.find(boundary)
    if n == -1:
      raise ValueError('unexpected EOF while parsing form-data')
    p = make_part(string[:n])
    multipart[p.name].append(p)
    if string[n:-2] == boundary + b'--':
        break
    string = string[len(boundary) + n + 2:]

  return multipart
