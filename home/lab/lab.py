'''

'''

import argparse
import json
import logging
import pathlib
import requests
import threading
import time

import serial
import toml

import dominate
import whirl
from dominate import tags
from whirl.domx import dx

import dl24
import xdm1041


log = logging.getLogger('lab')

config = toml.load("../config.toml")['grafana']

ROOT = pathlib.Path('.')

DEV = None


def post_grafana(ns, **kv):
  auth = 'Bearer {}:{}'.format(59684, config['grafana_token'])
  now = int(time.time())
  data = [{
    'name': '.'.join((ns, k)),
    'value': v,
    'time': now,
    'interval': 2,
  } for k,v in kv.items()]
  try:
    p = requests.post(
      config['grafana_uri'],
      headers={'Authorization': auth, 'Content-Type':'application/json'},
      json=data
    )
    log.info(p.json())
  except Exception as e:
    log.error(e)


@whirl.domx.template
class dl24dash(dominate.document):
  def __init__(self, *a, **kw):
    super(dl24dash, self).__init__('DL24Load', *a, **kw)

    self.head += tags.link(rel="stylesheet", href="https://cdn.simplecss.org/simple.min.css")
    self.head += tags.link(rel="stylesheet", href="https://unpkg.com/@picocss/pico@1.5.3/css/pico.min.css")

    self.head += tags.script(src='https://githubraw.com/Knio/dominate.js/master/dominate.js')

    self.head += tags.script(src='https://cdnjs.cloudflare.com/ajax/libs/remarkable/2.0.1/remarkable.min.js')
    self.head += tags.script(src='https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.6.0/highlight.min.js')
    self.head += tags.link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.6.0/styles/default.min.css")

    self.head += tags.style(dominate.util.include(ROOT / 'lab.css'))
    self.head += tags.script(dominate.util.include(ROOT / 'lab.js'))

    container = tags.main(cls='container')
    self.body += container
    self._entry = container


@whirl.domx.route('/')
@tags.div(cls='flex flex-row')
def index(url, handler, match):
  with tags.div(cls='basis-1/4'):
      tags.h2('hi')

  with tags.div(cls='flex basis-1/2 flex-col'):
    with tags.div(cls='flex'):
      # debug
      tags.div('Hello world')
      tags.button('test', dx(target='#test', get='/test'))
      tags.button('stop', dx(target='#test', get='/stop'))
      tags.div(id='test')

    tags.div('hi', id='task_insert', cls='flex')

    tags.h2('hi')

  tags.script(dominate.util.raw('''apply_markdown();'''))


@whirl.domx.route('/stop')
def route_content(url, handler, match):
  raise KeyboardInterrupt


@whirl.domx.route(r'/task/([^/]+)$')
def route_task(url, handler, match):
  task_id = match.group(1)
  return view_task(task_id)

dl_dev = None
xdm_dev = None


def poll_loop():
  start = time.time()
  count = 0


  while 1:
      count += 1

      global xdm_dev
      global dl_dev

      if dl_dev:
        try:
            dl_dev.flush()
            metrics = dl_dev.get_all()
            ds = json.dumps(metrics, indent=2)
            log.info(f'metrics {count}:\n{ds}')
            post_grafana('lab.dl24m', **metrics)
        except KeyboardInterrupt:
          break
        except:
            log.exception('error')

      if xdm_dev:
        mode = xdm_dev.get_mode()
        value = xdm_dev.get_value()
        metrics = {mode.name: value}
        log.info(f'metrics {count}: {metrics!r}')
        post_grafana('lab.xdm1041', **metrics)


      next = start + count * 1.0
      time.sleep(max(0.1, next - time.time()))



def main():
  print('hello world')

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('--dl24m', type=str)
  parser.add_argument('--xdm1041', type=str)
  args = parser.parse_args()

  if (args.dl24m):
    log.info(f'Using DL24M from {args.dl24m}')
    global dl_dev
    dl_dev = None
    ser = serial.Serial(args.dl24m, timeout=2.)
    dl_dev = dl24.DL24M(ser)
    dl_dev.get_state()


  if (args.xdm1041):
    log.info(f'Using XDM1041 from {args.xdm1041}')
    ser = serial.Serial(
      args.xdm1041,
      baudrate=115200,
      parity='N',
      bytesize=8,
      stopbits=1,
      timeout=1.
    )
    global xdm_dev
    xdm_dev = xdm1041.XDM1041(ser)

  poll_thread = threading.Thread(target=poll_loop)
  poll_thread.daemon = True
  poll_thread.start()

  whirl.domx.run(('', 8888))




if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    # level=logging.DEBUG,
    level=logging.INFO,
  )
  logging.getLogger('urllib3').setLevel(logging.WARNING)
  main()


