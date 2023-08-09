'''
Web frontend to control home devices

'''

import argparse
import logging
import time
import asyncio

import dominate
import requests
import whirl
from dominate import tags
from whirl.domx import dx

from devices import denon_avr

import kasa

amp = None

@whirl.domx.route('/')
@tags.div
def index(url, handler, match):
  tags.h1('Hello world')
  with tags.div(tags.h2('Sound')):
    tags.button('foo', dx(target='#content', get='/foo'))
    tags.button('bar', dx(target='#content', get='/bar'))
    tags.br()
    tags.button('on', dx(target='#content', get='/avr/on'))
    tags.button('off', dx(target='#content', get='/avr_off'))
    tags.br()
    for v in range(-70, -20, 5):
      tags.button(f'{v:2d}db', dx(target='#content', get=f'/avr/vol/{v}'))

  with tags.div(tags.h2('Lights')):
    for i in range(2):
      with tags.div(f'light {i}'):
        tags.button('on', dx(target='#content', get=f'/light/{i}/on'))
        tags.button('off', dx(target='#content', get=f'/light/{i}/off'))

  with tags.div(tags.h2('Music')):
    tags.button('play', dx(target='#content', get='/foobar/play'))
    tags.button('pause', dx(target='#content', get='/foobar/pause'))
    tags.button('random', dx(target='#content', get='/foobar/random'))


  with tags.div(id='content'):
    foo(None, None, None)

@whirl.domx.route('/foo')
@tags.div
def foo(url, handler, match):
  # p = 'over 9000'
  p = amp.get_power()
  tags.h3(f'Power?: {p}')
  time.sleep(0.1)
  v = amp.get_vol()
  tags.h3(f'Vol?: {v} dB')


@whirl.domx.route('/avr/on')
@tags.div
def avr_on(url, handler, match):
  amp.set_power(amp.PowerState.ON)
  tags.p('Power turned on')


@whirl.domx.route('/avr_off')
@tags.div
def avr_off(url, handler, match):
  amp.set_power(amp.PowerState.STANDBY)
  tags.p('Power turned off')

@whirl.domx.route('^/avr/vol/([+-]?\d+)$')
@tags.div
def avr_vol(url, handler, match):
  v = int(match.group(1))
  amp.set_vol(v)
  tags.p(f'Vol set to {v:d}')

@whirl.domx.route('^/light/(\d+)/(\w+)$')
def light(url, handler, match):
  l = int(match.group(1))
  s = match.group(2)
  if s == 'on':
    aiol.run_until_complete(lights[l].turn_on())
    tags.p(f'light {l} turned on')
  elif s == 'off':
    aiol.run_until_complete(lights[l].turn_off())
    tags.p(f'light {l} turned off')
  else:
    tags.p(f'bad command: {s!r}')

@whirl.domx.route('^/foobar/(\d+)$')
def foobar(url, handler, match):
  cmd = match.group(1)
  if cmd == 'play':
    r = requests.post('http://10.0.0.10:8880/api/player/play')
  elif cmd == 'pause':
    r = requests.post('http://10.0.0.10:8880/api/player/pause/toggle')
  elif cmd == 'random':
    r = requests.post('http://10.0.0.10:8880/api/player/play/random')
  else:
    tags.p(f'bad command: {cmd!r}')
    return
  tags.p(r.status_code)




def main():
  logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s')

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  args = parser.parse_args()

  global amp
  amp = denon_avr.DenonAVR('10.0.0.22')

  global lights
  lights = [
    kasa.SmartPlug('10.0.0.202'),
    kasa.SmartPlug('10.0.0.201'),
  ]
  # fuck you
  global aiol
  aiol = asyncio.get_event_loop()


  for l in lights:
    aiol.run_until_complete(l.update())

  whirl.domx.run(('', 8000))

if __name__ == '__main__':
  main()
