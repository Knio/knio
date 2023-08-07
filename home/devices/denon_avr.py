'''
Usage:

$env:PYTHONPATH = "."
knio\home> python .\devices\denon_avr.py

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


  def __init__(self, host):
    self.host = host
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.settimeout(0.1)
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
    return result

  def process(self, event):
    LOG.info(f'AVR: {event}')

  def query(self, query):
    self.poll(timeout=0)
    self.ser.write(f'{query}?\r'.encode('ascii'))
    return self.poll(query, timeout=0.1)

  def cmd(self, cmd, value):
    self.poll(timeout=0)
    s = f'{cmd}{value}\r'
    self.ser.write(s.encode('ascii'))

  def get_power(self):
    LOG.info('get_power')
    r = self.query('PW')
    return self.PowerState[r[2:]]
    return r

  def set_power(self, pw):
    # pw = self.PowerState[pw]
    self.cmd('PW', pw.name)

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
    self.cmd('MV', f'{v:02d}')


def main():
  import argparse

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('--ip', type=str, default='10.0.0.22')
  args = parser.parse_args()

  amp = DenonAVR(args.ip)
  print(amp.get_power())


if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
  )
  main()
