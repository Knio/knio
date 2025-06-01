'''
Accepts HTTP form uploads and saves them to a directory.
'''
import argparse
import datetime
import logging
import pathlib

import whirl
import whirl.parsers


import page

LOG = logging.getLogger()

import toml
import pathlib
CONF = toml.load(pathlib.Path(__file__).parent.parent / 'config.toml')
IRC = CONF['irc']



@whirl.domx.route('/upload')
def index(url, handler):
  return page.uploadui()


@whirl.domx.route('/updo')
def upload(url, handler):
  LOG.debug(f'headers: {handler.headers}')
  LOG.debug(f'client_address: {handler.client_address}')

  n = int(handler.headers.get('Content-Length', 0))
  ct = handler.headers.get('Content-Type', '')
  LOG.debug(f'content-type: {ct}')
  LOG.debug(f'receving {n:,} bytes...')

  assert handler.command == 'POST'
  data = handler.rfile.read(n)

  if 'multipart/form-data' in ct:
    msg = whirl.parsers.parse_multipart(ct, data)
    LOG.debug(f'{msg.keys()=}')
    try:
      toirc = msg.pop('toirc')[0]
      toirc = toirc.data.decode('ascii').lower() not in ('', '0', 'no', 'false')
    except (KeyError, IndexError) as e:
      LOG.debug(e)
      toirc = False
    urls = []
    for k, items in msg.items():
      for v in items:
        LOG.debug(f'{k=}')
        LOG.debug(f'{v.headers=}')
        LOG.debug(f'{v.name=}')
        LOG.debug(f'{v.disposition=}')
        LOG.debug(f'{v.data[:200]=!r}')
        u = save_msg(v, toirc)
        urls.append(u)

    # TODO html
    # TODO redirect back to upload
    return ' '.join(urls)

  return "not cool"


def save_msg(msg, toirc):
  ct = msg.headers.get('Content-Type', '')
  now = datetime.datetime.now()
  dir = ARGS.dir / now.date().isoformat()

  fn = msg.disposition.get('filename')
  is_file = fn is not None
  if fn is None:
    dt = datetime.datetime.now().isoformat()
    fn = f'{dt}.{ct.split("/")[-1]}'
  fn = pathlib.Path(fn).name
  f = dir / fn
  while f.exists():
    f = f.with_stem(f.stem + '.1')
  f.parent.mkdir(parents=True, exist_ok=True)
  f.write_bytes(msg.data)
  LOG.info(f'saved {f}')
  url = f'https://img.zkpq.ca/{f.relative_to(ARGS.dir)}'
  if is_file and toirc:
    post_irc(url)
  return url


def post_irc(msg):
  import http.client
  conn = http.client.HTTPConnection(IRC['host'], IRC['port'])
  conn.request('POST', '/privmsg/deviate/',
      headers=IRC['headers'],
      body=msg,
  )
  r = conn.getresponse()
  if r.status != 200:
    LOG.warning(f'irc: {r.status!s} {r.msg}')
  LOG.info(f'irc: " {r.read()}')


def parse_args():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)
  parser.add_argument('--port', type=int, default=8005)
  parser.add_argument('--dir', type=pathlib.Path, default='.')
  args = parser.parse_args()
  return args


def main():
  whirl.domx.run(('', ARGS.port))


if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(funcName)s %(message)s',
    datefmt='%y%m%d-%H%M%S',
    level=logging.DEBUG,
  )
  ARGS = parse_args()
  main()
