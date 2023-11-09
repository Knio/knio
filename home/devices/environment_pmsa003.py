
import argparse
import enum
import logging
import struct
import time

import serial

from devices import utils

LOG = logging.getLogger(__name__)


class PMSA0004:
  pass





def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('port', type=str, default='COM13')
  args = parser.parse_args()

  # cmd = RadarLD2410.Command()
  # print(cmd)

  ser = serial.Serial(
    args.port,
    baudrate=9600,
    parity='N',
    bytesize=8,
    stopbits=1,
    timeout=.1
  )
  ss = utils.PySerial(ser, timeout=0.1)

  try:
    while 1:
      b = ss.read()
      print(f'read: {b.hex(" ")}')

  except KeyboardInterrupt:
    pass


# to run: (from parent dir)
# python -m devices.radar_ld2410 COM13

if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
  )
  main()

