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

import dl24
import dominate
import whirl
from dominate import tags


log = logging.getLogger('lab')

config = toml.load("config.toml")['lab']

ROOT = pathlib.Path('.')


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

    container = main(cls='container')
    self.body += container
    self._entry = container


@whirl.domx.route('/')
@div(cls='flex flex-row')
def index(url, handler, match):
  with div(cls='basis-1/4'):
      view_tasks(finished=True)

  with div(cls='flex basis-1/2 flex-col'):
    with div(cls='flex'):
      # debug
      div('Hello world')
      button('test', dx(target='#test', get='/test'))
      button('stop', dx(target='#test', get='/stop'))
      div(id='test')

    div(add_task(), id='task_insert', cls='flex')

    view_tasks()

  script(util.raw('''apply_markdown();'''))


@whirl.domx.route('/stop')
def route_content(url, handler, match):
  raise KeyboardInterrupt


@whirl.domx.route('/test')
def route_content(url, handler, match):
  return div('foobar')


@whirl.domx.route('/tasks')
def route_tasks(*args):
  return view_tasks()


@whirl.domx.route(r'/task/([^/]+)$')
def route_task(url, handler, match):
  task_id = match.group(1)
  return view_task(task_id)





def main():
  print('hello world')

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('port', type=str, default='COM9')
  args = parser.parse_args()

  ser = serial.Serial(
    args.port,
    # baudrate=9600,
    # bytesize=8,
    # stopbits=1,
    timeout=2.
  )

  dev = dl24.DL24M(ser)
  start = time.time()
  count = 0
  while 1:
      count += 1
      try:
          dev.flush()
          metrics = dev.get_all()
          ds = json.dumps(metrics, indent=2)
          log.info(f'metrics {count}:\n{ds}')
          post_grafana('lab.load', **metrics)
      except KeyboardInterrupt:
        break
      except:
          log.exception('error')

      next = start + count * 1.0
      time.sleep(max(0.1, next - time.time()))

  whirl.domx.main()



if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    # level=logging.DEBUG,
    level=logging.INFO,
  )
  logging.getLogger('urllib3').setLevel(logging.WARNING)
  main()


