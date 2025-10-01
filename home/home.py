'''
Web frontend to control home devices

'''

import argparse
import logging
import pathlib
import requests
import dominate
import whirl
from dominate import tags
from whirl.domx import dx

from devices import denon_avr
from devices import kasa


LOG = logging.getLogger('home')

root = pathlib.Path(__file__).parent

home = None

@whirl.domx.template
class HomePage(dominate.document):
  def __init__(self, title='Home', *a, **kw):
    super().__init__(title, *a, **kw)
    with self.head:
      tags.style(dominate.util.include('home.css'))


header = lambda x:tags.h2(tags.span(x))

@whirl.domx.route('/')
@tags.div
def index(url, handler):
  tags.h1('Hello world')

  with tags.div(header('Scene')):
    with tags.div():
      for s in ('Active', 'Work', 'Lounge', 'Movie', 'Sleep', 'Gone'):
        tags.button(s, dx(target='#content', get=f'/scene/{s.lower()}'))

  with tags.div(header('Sound')):

    with tags.div('power'):
      tags.button('on', dx(target='#content', get='/avr/on'))
      tags.button('off', dx(target='#content', get='/avr_off'))
    with tags.div('volume'):
      for v in range(-70, -20, 5):
        tags.button(f'{v:2d}db', dx(target='#content', get=f'/avr/vol/{v}'))
    with tags.div('source'):
      for s in ('TV', 'NET'):
        tags.button(s, dx(target='#content', get=f'/avr/si/{s}'))

  with tags.div(header('Lights')):
    for k, v in home.lights.items():
      with tags.div(f'light {k}'):
        tags.p(k)
        tags.input_(dx(target='#content', get=f'/light/{k}/on'), type="checkbox")
        tags.button('on', dx(target='#content', get=f'/light/{k}/on'))
        tags.button('off', dx(target='#content', get=f'/light/{k}/off'))

  with tags.div(header('Music')):
    with tags.div():
      for c in ('play', 'pause', 'random'):
        tags.button(c, dx(target='#content', get=f'/foobar/{c}'))

  with tags.div(id='content'):
    foo(url, handler)


@whirl.domx.route(r'^/foo$')
@tags.div
def foo(url, handler):
  with home.do_amp() as a:
    p = a.get_power()
    tags.h3(f'Power?: {p}')

    v = a.get_vol()
    tags.h3(f'Vol?: {v} dB')

    s = a.get_source()
    tags.h3(f'Source?: {s}')


@whirl.domx.route(r'^/avr/on$')
@tags.div
def avr_on(url, handler):
  with home.do_amp() as a:
    a.set_power(a.PowerState.ON)
  tags.p('Power turned on')


@whirl.domx.route(r'^/avr_off$')
@tags.div
def avr_off(url, handler):
  with home.do_amp() as a:
    a.set_power(a.PowerState.STANDBY)
  tags.p('Power turned off')


@whirl.domx.route(r'^/avr/vol/([+-]?\d+)$')
@tags.div
def avr_vol(url, handler, vol):
  v = int(vol)
  with home.do_amp() as a:
    a.set_vol(v)
  tags.p(f'Vol set to {v:d}')

@whirl.domx.route(r'^/avr/si/(\w+)$')
@tags.div
def avr_si(url, handler, si):
  with home.do_amp() as a:
    a.set_source(si)
  tags.p(f'Source set to {si}')


@whirl.domx.route(r'^/light/([\w]+)/(\w+)$')
def light(url, handler, id, state):
  if state == 'on':
    home.lights[id].turn_on()
    tags.p(f'light {id} turned on')
  elif state == 'off':
    home.lights[id].turn_off()
    tags.p(f'light {id} turned off')
  else:
    tags.p(f'bad command: {state!r}')

@whirl.domx.route(r'^/foobar/(\w+)$')
def foobar(url, handler, cmd):
  LOG.info(url)
  # TODO: move this to devices.foobar
  if cmd == 'play':
    r = requests.post('http://10.87.1.10:8880/api/player/play', timeout=1)
  elif cmd == 'pause':
    r = requests.post(
      'http://10.87.1.10:8880/api/player/pause/toggle', timeout=1)
  elif cmd == 'random':
    r = requests.post('http://10.87.1.10:8880/api/player/play/random', timeout=1)
  else:
    tags.p(f'bad command: {cmd!r}')
    return
  tags.p(r.status_code)


@whirl.domx.route(r'^/scene/(\w+)$')
def scene(url, handler, cmd):
  LOG.info(url)
  r = getattr(home, f'scene_{cmd}')()
  tags.p(f'{r!r}')


class Home:
  def __init__(self):
    self.amp = denon_avr.DenonAVR('10.87.1.17')
    self.lights = dict(
      office=kasa.SmartDimmer('10.87.1.51'),
      shop=kasa.SmartDimmer('10.87.1.52'),
      outside=kasa.SmartDimmer('10.87.1.53'),
      # kasa.SmartPlug('10.87.1.42'),
    )
    self.radar = None

  # pylint: disable=no-self-argument
  def do_amp(h):
    class AmpTry:
      def __enter__(self):
        return h.amp
      def __exit__(self, exec_type, exc_val, exc_tb):
        if exec_type is not None:
          h.amp.reset()
    return AmpTry()

  def scene_active(self):
    with self.do_amp() as a:
      a.set_power(a.PowerState.ON)
      a.set_source('TV')
      a.set_z2('OFF')
      a.set_vol(-50)
    self.lights[0].turn_on()
    self.lights[1].turn_on()
    return True

  def scene_work(self):
    with self.do_amp() as a:
      a.set_power(a.PowerState.ON)
      a.set_source('TV')
      a.set_z2('OFF')
      a.set_vol(-55)
    self.lights[0].turn_on()
    self.lights[1].turn_on()
    requests.post('http://10.87.1.10:8880/api/player/play', timeout=1)
    return True

  def scene_lounge(self):
    with self.do_amp() as a:
      a.set_power(a.PowerState.ON)
      a.set_source('TV')
      a.set_z2('OFF')
      # TODO: move this to devices.foobar
      requests.post('http://10.87.1.10:8880/api/player/play', timeout=1)
      a.set_vol(-55)
    self.lights[0].turn_on()
    self.lights[1].turn_off()
    return True

  def scene_movie(self):
    # TODO pause foobar
    with self.do_amp() as a:
      a.set_source('NET')
      a.set_z2('OFF')
    self.lights[0].turn_off()
    self.lights[1].turn_off()
    return True

  def scene_sleep(self):
    self.lights[0].turn_off()
    self.lights[1].turn_off()
    return True

  def scene_gone(self):
    # TODO: move this to devices.foobar
    requests.post('http://10.87.1.10:8880/api/player/pause/toggle', timeout=1)
    return True


def main():
  logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s')

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  args = parser.parse_args()

  global home
  home = Home()

  whirl.domx.run(('', 8888))

if __name__ == '__main__':
  main()
