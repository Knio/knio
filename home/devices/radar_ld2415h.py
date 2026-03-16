
import argparse
import enum
import logging
import struct
import time

import serial

from devices import utils
from devices import datum

LOG = logging.getLogger(__name__)

# pyright: reportInvalidTypeForm=false

class LDCommand(datum.Datum):
  header:   datum.u32(endian='little') = 0xFDFCFBFA
  length:   datum.u16(endian='little')
  command:  datum.u16(endian='little')
  data:     datum.array(datum.u8(endian='little'), length='length', bias=-2)
  footer:   datum.u32(endian='little') = 0x04030201


class LDAck(LDCommand):
  pass


class LDTarget(datum.Datum):
  angle:      datum.u8(endian='little')
  distance:   datum.u8(endian='little')
  sign:       datum.u8(endian='little')
  speed:      datum.u8(endian='little')
  snr:        datum.u8(endian='little')


class LDTargets(datum.Datum):
  ntargets: datum.u8(endian='little')
  alarm:    datum.u8(endian='little')
  data:     datum.array(LDTarget, length='ntargets')


class LDReport(datum.Datum):
  header:   datum.u32(endian='little') = 0xF4F3F2F1
  length:   datum.u16(endian='little')
  data:     datum.array(datum.u8(endian='little'), length='length')
  footer:   datum.u32(endian='little') = 0xF8F7F6F5



class RadarLD2451:
  def __init__(self, ser):
    self.ser = ser


  def poll(self):
    b = self.ser.read_all()
    if not b: return
    LOG.debug(b.hex(' ', 4))
    return
    try:
      f, r = LDReport.deserialize_new(b)
      if r.data:
        t = LDTargets.deserialize_new(f.data)
        return t
    except:
      LOG.exception(f'Failed to parse. {b=}')


def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('port', type=str, default='COM9')
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

  ld = RadarLD2451(ss)
  last = time.time()
  try:
    while 1:
      now = time.time()
      frame = ld.poll()
      if not frame:
        continue
      LOG.debug(f'{frame=}')
      if now > last + 1:
        # post_grafana('radar_ld2410', **frame)
        last = now

  except KeyboardInterrupt:
    pass


# to run: (from parent dir)
# python -m devices.radar_ld2415h COM9

if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
  )
  main()
