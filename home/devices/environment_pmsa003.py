'''

PINS
                     _________
                VCC -| 1   2 |- VCC
                GND -| 3   4 |- GND                n/c
        RESET (3v3) -| 5   6 |- N/C
           RX (3v3) -| 7   8 |- N/C
           TX (3v3) -| 9  10 |- SET (3v3)
                     ‾‾‾‾‾‾‾‾‾

SET - pull high internally
RESET - pulled high internally


'''


import argparse
import logging
import struct

import serial

from devices import utils

LOG = logging.getLogger(__name__)


class PMSA0004:
  u8 = 'B'
  u16 = 'H'
  # TODO use datum
  _frame = dict(
    start = u16,
    length = u16,

    pm01_0_ug_m3_cf = u16,
    pm02_5_ug_m3_cf = u16,
    pm10_0_ug_m3_cf = u16,

    pm01_0_ug_m3_atm = u16,
    pm02_5_ug_m3_atm = u16,
    pm10_0_ug_m3_atm = u16,

    pm00_3_dl = u16,
    pm00_5_dl = u16,
    pm01_0_dl = u16,
    pm02_5_dl = u16,
    pm05_0_dl = u16,
    pm10_0_dl = u16,

    version = u8,
    error = u8,
    crc = u16,

  )

  Frame = struct.Struct(
    '!' +
    ''.join(_frame.values())
  )

  length = Frame.size

  def __init__(self, ss):
    self.serial = ss
    self.serial.timeout = 0.5

  def poll(self):
    # TODO need a .read_n()
    d = self.serial.read_all()
    LOG.debug(f'{len(d)} {d.hex(" ")}')
    if len(d) != self.Frame.size:
      LOG.info(f'Ignoring incomplete data: ({len(d)} != {self.Frame.size}): {d.hex()}')
      return

    vals = self.Frame.unpack(d)
    return dict(zip(self._frame.keys(), vals))


def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('port', type=str, default='COM18')
  args = parser.parse_args()

  ser = serial.Serial(
    args.port,
    baudrate=9600,
    parity='N',
    bytesize=8,
    stopbits=1,
    timeout=.1
  )
  ss = utils.PySerial(ser, timeout=0.1)
  pms = PMSA0004(ss)

  try:
    while 1:
      # b = ss.read()
      # print(f'read: {b.hex(" ")}')
      print(pms.poll())

  except KeyboardInterrupt:
    pass


# to run: (from parent dir)
# python -m devices.environment_pms003 COM18

if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    # level=logging.DEBUG,
    level=logging.INFO,
  )
  main()
