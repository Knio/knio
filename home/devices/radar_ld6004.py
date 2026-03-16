
import argparse
import enum
import logging
import struct
import time

import serial

from devices import utils
from devices import datum


LOG = logging.getLogger('LD6001')

Command = datum.datum_bigint(size=1, signed=False)



def crc(dat, buf, i, parent):
  crc = sum(buf[0:i]) & 0xff
  dat.set_value(crc)

# pyright: reportInvalidTypeForm=false
class LD6Frame(datum.Datum):
  SOF_DEVICE = 0x4D
  EOF_DEVICE = 0x4A

  sof:      datum.u8 = 0x44

class Radar:
  def __init__(self, ser):
    self.ser = ser

  def poll(self):
    b = self.ser.read_all() # TODO implement datum partial reads
    if not b: return

    LOG.debug(f'RX: {b.hex(" ", 8)}')
    # if (i := b.find(LD6Frame.SOF_DEVICE)) == -1:
    #   return
    # b = b[i:]

    return
    f, more = LD6Frame.deserialize_new(b)
    match f.command:
      case LD6001InfoQuery.ID:
        r, _ = LD6001InfoResponse.deserialize_new(f.data)
      case LD6001RadarQuery.ID:
        r, _ = LD6001RadarData.deserialize_new(f.data)
      case _:
        r = f

    self.ser.push(more)
    return r


def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('port', type=str, default='COM13')
  args = parser.parse_args()

  ser = serial.Serial(
    args.port,
    baudrate=115200,
    parity='N',
    bytesize=8,
    stopbits=1,
    timeout=.1
  )
  ss = utils.PySerial(ser, timeout=0.1)

  ld = Radar(ss)

  last = time.time()
  try:
    while 1:
      now = time.time()
      frame = ld.poll()
      if not frame:
        continue
      LOG.info(f'{frame=}')
      if now > last + 1:
        last = now
      time.sleep(1)

  except KeyboardInterrupt:
    pass


# to run: (from parent dir)
# python -m devices.radar_ld6001 COM13

if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
  )
  main()
