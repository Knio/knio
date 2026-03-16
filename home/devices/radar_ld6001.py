
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
  command:  datum.u8
  length:   datum.u8
  reserved: datum.u8 = 0
  data:     datum.array(datum.u8, length='length')
  crc:      datum.u8(cb=crc)
  eof:      datum.u8 = 0x4B


class LD6001InfoQuery(datum.Datum):
  ID = 0x11


class LD6001InfoResponse(datum.Datum):
  sw_min:   datum.u8
  sw_maj:   datum.u8
  hw_min:   datum.u8
  hw_maj:   datum.u8
  reserved: datum.u8
  status:   datum.u8
  reserved1:datum.u8
  reserved2:datum.u8


class LD6001RadarQuery(datum.Datum):
  ID = 0x62
  sensitivity: datum.u8 = 0x10
  z:   datum.datum_bigint(size=7)


class LD6001Target(datum.Datum):
  id:           datum.u8
  distance_dm:  datum.u8
  pitch_deg:    datum.u8
  yaw_deg:      datum.u8
  z:            datum.u16
  x:            datum.i8
  y:            datum.i8


class LD6001RadarData(datum.Datum):
  fault:  datum.u8
  n:      datum.u8
  z:      datum.datum_bigint(size=6)
  targets: datum.array(LD6001Target, length='n')


class Radar:
  def __init__(self, ser):
    self.ser = ser


  def query_info(self):
    q = LD6001InfoQuery()
    cmd = LD6Frame(command=q.ID)
    b = cmd.serialize()
    self.ser.write(b)
    LOG.debug(f'TX: {b.hex(" ", 8)}')

  def query_targets(self):
    q = LD6001RadarQuery()
    cmd = LD6Frame(command=q.ID)
    b = cmd.serialize()
    self.ser.write(b)
    LOG.debug(f'TX: {b.hex(" ", 8)}')

  def poll(self):
    b = self.ser.read_all() # TODO implement datum partial reads
    if not b: return

    if (i := b.find(LD6Frame.SOF_DEVICE)) == -1:
      return
    b = b[i:]

    LOG.debug(f'RX: {b.hex(" ", 8)}')
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
    baudrate=9600,
    parity='E',
    bytesize=8,
    stopbits=1,
    timeout=.1
  )
  ss = utils.PySerial(ser, timeout=0.1)

  ld = Radar(ss)
  ld.query_info()

  last = time.time()
  try:
    while 1:
      now = time.time()
      ld.query_targets()
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
    # level=logging.DEBUG,
    level=logging.INFO,
  )
  main()
