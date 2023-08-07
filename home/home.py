'''
Web frontend to control home devices

'''

import argparse
import logging
import time

import dominate
import whirl
from dominate import tags
from whirl.domx import dx

from devices import denon_avr


amp = None

@whirl.domx.route('/')
@tags.div
def index(url, handler, match):
  tags.h1('Hello world')
  tags.button('foo', dx(target='#content', get='/foo'))
  tags.button('bar', dx(target='#content', get='/bar'))
  tags.br()
  tags.button('on', dx(target='#content', get='/avr/on'))
  tags.button('off', dx(target='#content', get='/avr_off'))
  tags.br()
  for v in range(-70, -20, 5):
    tags.button(f'{v:2d}db', dx(target='#content', get=f'/avr/vol/{v}'))

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


def main():
  logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s')

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  args = parser.parse_args()

  global amp
  amp = denon_avr.DenonAVR('10.0.0.22')

  whirl.domx.run(('', 8000))

if __name__ == '__main__':
  main()
