'''
Usage:

$Env:PYTHONPATH = "."
knio\home> python .\devices\denon_avr.py


or maybe:

# python -m devices.denon_avr COM13

'''

import enum
import socket
import logging
import math
import time
import re

from devices import utils


LOG = logging.getLogger(__name__)

class DenonAVR:

  class PowerState(enum.Enum):
    STANDBY = 1
    ON = 2

  class SourceInput(enum.StrEnum):
    '''
        SITUNER
        SIDVD
        SIBD
        SITV
        SISAT/CBL
        SISMPLAY
        GAMESIGAME
        SIAUX1
        SINET
        SIPANDORA
        SISIRIUSXM
        SISPOTIFY
        SIFLICKR
        SIFAVORITES
        SIIRADIO
        SISERVER
        SIUSB/IPOD
        SIIPD
        SIIRP
        SIFVP
    '''
    COMPUTER = 'TV'


  def __init__(self, host):
    self.host = host
    self.reset()

  def reset(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.settimeout(0.2) # for connect
    self.socket.connect((self.host, 23))
    self.ser = utils.SocketSerial(self.socket)
    self.queue = []

  def flush(self, prefix=None, timeout=None):
    # self.ser.write(b'\r')
    events = []
    result = None
    done = False
    while not done:
      LOG.debug(f'f {timeout}')
      r = self.ser.read_until(b'\r', 0).decode('ascii')
      LOG.debug(f'flush: {r!r}')
      if not r:
        r = self.ser.read_until(b'\r', timeout).decode('ascii')
        LOG.debug(f'flush: {r!r}')
        done = True
        if not r:
          break
      if prefix and r.startswith(prefix):
        result = r[:-1]
        prefix = None
      events.append(r)
    return events, result

  def poll(self, prefix=None, timeout=None):
    events, result = self.flush(prefix, timeout)
    for event in events:
      self.process(event)
    if prefix and (result is None):
      raise TimeoutError(f'timeout waiting for {prefix!r} response')
    return result

  def process(self, event):
    LOG.info(f'AVR: {event}')

  def query(self, query):
    self.poll(timeout=0.1)
    self.ser.write(f'{query}?\r'.encode('ascii'))
    return self.poll(query, timeout=0.1)

  def cmd(self, cmd, value):
    self.poll(timeout=0)
    s = f'{cmd}{value}\r'
    self.ser.write(s.encode('ascii'))
    self.poll(timeout=0.05)

  def get_power(self):
    LOG.info('get_power')
    r = self.query('PW')
    return self.PowerState[r[2:]]

  def get_source(self):
    r = self.query('SI')
    return r

  def set_source(self, si):
    return self.cmd('SI', si)

  def set_power(self, pw):
    return self.cmd('PW', pw.name)


  def set_z2(self, cmd):
    return self.cmd('Z2', cmd)

  def get_vol(self):
    LOG.info('get_vol')
    r = self.query('MV')
    m = re.match(r'^MV(\d+)$', r)
    if m:
      return int(m.group(1)) - 80
    LOG.error(r)
    return None

  def set_vol(self, db):
    # TODO .5db steps
    v = int(round(db))
    v = max(min(v, 18), -80)
    v += 80
    return self.cmd('MV', f'{v:02d}')


def main():
  import argparse

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('--host', type=str, default='denon-avr-x2400h.home')
  args = parser.parse_args()

  amp = DenonAVR(args.host)
  print(amp.get_power())
  amp.set_z2('OFF')
  amp.set_power(DenonAVR.PowerState.STANDBY)


if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
  )
  main()
