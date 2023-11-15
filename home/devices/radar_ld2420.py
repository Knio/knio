'''
to run: (from parent dir)

python -m devices.radar_ld2420 COM13

'''
import logging
import re
import time

import serial

from devices import utils

LOG = logging.getLogger(__name__)


class RadarLD2420:

  def __init__(self, ser):
    self.ser = ser
    self.ser.timeout = 0.001
    self.range = 0
    self.time = 0

  def poll(self):
    now = time.time()
    while 1:
      data = self.ser.read_until(b'\r\n')
      if data == b'':
        break
      try:
        data = data.decode('ascii').strip()
      except:
        LOG.info('corrupted data: %r', data)
        continue
      if data in {None, 'ON', 'OFF'}:
        continue
      if m := re.match(r'^Range (\d+)$', data):
        self.range = int(m.group(1))
        self.time = time.time()

    if now > self.time + 1:
      return None
    return self.range


#pylint: disable=import-outside-toplevel
def parse_args():
  import argparse

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('port', type=str, default='COM13', nargs='+')
  return parser.parse_args()

def main(args):
  import threading

  import grafana

  def loop(radar, name):
    last = time.time()
    while 1:
      now = time.time()
      frame = radar.poll()
      print(f'{name}: {frame}')
      if frame and now > last + 0.25:
        grafana.post(f'radar.{name}', range=frame)
        last = now

  for i, port in enumerate(args.port):
    ser = serial.Serial(
      port,
      baudrate=115200,
      parity='N',
      bytesize=8,
      stopbits=1,
      timeout=.5
    )
    ss = utils.PySerial(ser, timeout=0.5)

    ld2410 = RadarLD2420(ss)
    t = threading.Thread(target=loop, args=(ld2410, f'{i}'))
    t.daemon = True
    t.start()

  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    pass

if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
  )
  main(parse_args())
