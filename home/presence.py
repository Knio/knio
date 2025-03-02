

import enum
import logging
import threading
import time

import serial

from devices import radar_ld2420
from devices import utils

LOG = logging.getLogger('presence')


class Location(enum.IntEnum):
  UNKNOWN = 0
  COMPUTER = 1
  COUCH = 2
  BED = 3


class Presence:
  # mapping of valid distances per radar
  locations = {
    Location.COMPUTER: [
      range(90, 190),
      range(50, 120),
      range(0, 900),
    ],
    Location.COUCH: [
      range(290, 420),
      range(320, 500),
      range(290, 460),
    ],
    Location.BED: [
      list(range(390, 580)) + [0],
      list(range(330, 450)) + [0],
      range(500, 600),
    ],
  }

  def __init__(self, ports):
    self.radars = []
    self.status = [(0, 0) for _ in ports]
    for port in ports:
      ser = serial.Serial(
        port,
        baudrate=115200,
        parity='N',
        bytesize=8,
        stopbits=1,
        timeout=.5
      )
      ss = utils.PySerial(ser, timeout=0.5)
      s = radar_ld2420.RadarLD2420(ss)
      self.radars.append(s)

  def start(self):
    def loop():
      while 1:
        now = time.time()
        for i, r in enumerate(self.radars):
          d = r.poll()
          if d:
            LOG.debug(f'radar {i}: {d}')
            self.status[i] = (now, d)

    t = threading.Thread(target=loop)
    t.daemon = True
    t.start()
    # self.thread = t

  def poll(self):
    now = time.time()
    to = now - 2
    result = {
      f'radar.{i}': d
      for i, (t, d) in enumerate(self.status) if t > to
    }

    status = Location.UNKNOWN
    for location, ranges in self.locations.items():
      ok = True
      for (t, d), r in zip(self.status, ranges):
        if t < to:
          d = 0
        if d not in r:
          ok = False
      if ok:
        status = location

    result['location'] = status
    return result

def main(args):
  #pylint: disable=import-outside-toplevel
  import json
  import grafana

  p = Presence(['COM14', 'COM21', 'COM16'])
  p.start()
  last = time.time()
  while 1:
    now = time.time()
    time.sleep(0.1)
    status = p.poll()
    if status['location'] == Location.UNKNOWN:
      LOG.info('\n' + json.dumps(status, indent=2, sort_keys=True))
    if now >= last + 1.1:
      grafana.post('presence', **status)
      last = now


def parse_args():
  pass


if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    # level=logging.DEBUG,
    level=logging.INFO,
  )
  main(parse_args())
