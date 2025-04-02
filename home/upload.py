'''
Accepts HTTP form uploads and saves them to a directory.
'''
import argparse
import datetime
import logging
import pathlib

import whirl
import whirl.parsers


LOG = logging.getLogger()


@whirl.domx.route('/')
def index(url, handler):
  # TODO html form
  return "ok"


@whirl.domx.route('/upload')
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
    for k, v in msg.items():
      LOG.debug(f'{k=}')
      LOG.debug(f'{v.headers=}')
      LOG.debug(f'{v.name=}')
      LOG.debug(f'{v.disposition=}')
      LOG.debug(f'{v.data[:200]=!r}')
      save_msg(v)
    return "ok"
  return "ok"


def save_msg(msg):
  ct = msg.headers.get('Content-Type', '')
  now = datetime.datetime.now()
  dir = args.dir / now.date().isoformat()

  fn = msg.disposition.get('filename')
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


def parse_args():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)
  parser.add_argument('--port', type=int, default=8801)
  parser.add_argument('--dir', type=pathlib.Path, default='.')
  args = parser.parse_args()
  return args


def main(args):
  whirl.domx.run(('', args.port))


if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(funcName)s %(message)s',
    datefmt='%y%m%d-%H%M%S',
    level=logging.DEBUG,
  )
  args = parse_args()
  main(args)
