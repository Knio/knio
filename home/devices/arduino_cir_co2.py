'''
to run: (from parent dir)

python -m devices.radar_ld2420 COM13

'''
import logging
import time
import json

import serial

from devices import utils

LOG = logging.getLogger(__name__)

class CO2:
  def __init__(self, ser):
    self.ser = ser

  def poll(self):
    line = self.ser.read_until(b'\n').decode('utf8')
    if not line:
      LOG.debug('timed out reading line')
      return
    try:
      data = json.loads(line)
    except json.decoder.JSONDecodeError:
      LOG.error('Could not parse line as json: %r', line)
      return
    return data.get('SCD30', None)


def main(args):
  import threading

  import grafana

  def loop(co2):
    now = time.time()
    data = co2.poll()
    if not data:
      return
    LOG.info(data)
    grafana.post('scd', **data)

  ser = serial.Serial(
    args.port,
    baudrate=9600,
    parity='N',
    bytesize=8,
    stopbits=1,
  )
  ss = utils.PySerial(ser, timeout=5)

  co2 = CO2(ss)

  try:
    while True:
      loop(co2)
  except KeyboardInterrupt:
    pass


#pylint: disable=import-outside-toplevel
def parse_args():
  import argparse

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('port', type=str)
  return parser.parse_args()



if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
  )
  main(parse_args())
