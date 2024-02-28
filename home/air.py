

import argparse
import logging

import serial

from devices import environment_pmsa003
from devices import utils

LOG = logging.getLogger('air')


def main(args):
  #pylint: disable=import-outside-toplevel
  import grafana

  ser = serial.Serial(
    args.port,
    baudrate=9600,
    parity='N',
    bytesize=8,
    stopbits=1,
    timeout=.1
  )
  ss = utils.PySerial(ser)
  p = environment_pmsa003.PMSA0004(ss)
  while 1:
    status = p.poll()
    if status is None:
      continue
    grafana.post('air', **status)


def parse_args():
  parser = argparse.ArgumentParser(
  formatter_class=argparse.RawTextHelpFormatter,
  description=__doc__)
  parser.add_argument('port', type=str, default='COM18')
  args = parser.parse_args()
  return args


if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    # level=logging.DEBUG,
    level=logging.INFO,
  )
  main(parse_args())
