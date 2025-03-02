'''
XDM1041 interface

Thanks to https://github.com/TheHWcave/OWON-XDM1041/blob/main/SCPI/XDM1041-SCPI.pdf

'''

import argparse
import enum
import logging
import time

import serial

LOG = logging.getLogger(__name__)




class XDM1041:

  class Mode(enum.Enum):
    VOLTAGE_DC    = b'VOLT'
    VOLTAGE_AC    = b'VOLT:AC'
    CURRENT_DC    = b'CURR'
    CURRENT_AC    = b'CURR:AC'
    RESISTANCE    = b'RES'
    CAPACITANCE   = b'CAP'
    FREQUENCY     = b'FREQ'
    PERIOD        = b'PER'
    DIODE         = b'DIOD'
    CONTINUITY    = b'CONT'
    TEMPERATURE   = b'TEMP:RTD'

  # TODO ranges
  NONE_VALUE = b'NONe'

  def __init__(self, ser):
    self.ser = ser

  def query(self, q):
    self.ser.write(q + b'?\n')
    return self.ser.readline().strip()

  def get_id(self):
    return self.query(b'*IDN').decode('ascii').split(',')

  def get_mode(self):
    m = self.query(b'FUNC?')
    m = m[1:-1].replace(b' ', b':')
    return self.Mode(m)

  def get_value(self):
    r = self.query(b'MEAS?')
    if r == self.NONE_VALUE:
      return None
    return float(r)

  def get_value_string(self):
    return self.query(b'MEAS:SHOW?')

  def get_aux_value(self):
    r = self.query(b'MEAS2?')
    if r == self.NONE_VALUE:
      return None
    return float(r)

  def get_aux_value_string(self):
    return self.query(b'MEAS2:SHOW?')


  def foo(self):
    while 1:
      print(self.get_id())
      print(self.get_mode())
      print(self.get_value())
      print(self.get_value_string())
      print(self.get_aux_value())
      print(self.get_aux_value_string())
      time.sleep(1)

def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('port', type=str, default='COM9')
  args = parser.parse_args()

  ser = serial.Serial(
    args.port,
    baudrate=115200,
    parity='N',
    bytesize=8,
    stopbits=1,
    timeout=1.
  )


  xdm = XDM1041(ser)
  xdm.foo()


if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
  )
  main()
