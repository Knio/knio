
import argparse
import enum
import logging
import struct
import time

import serial

from devices import utils
from devices import datum


LOG = logging.getLogger('R24B')

Command = datum.datum_bigint(size=3, signed=False)

# pyright: reportInvalidTypeForm=false
class R24Frame(datum.Datum):
  start:    datum.u8 = 0x55
  length:   datum.u16le
  command:  Command
  data:     datum.array(datum.u8, length='length', bias=-7)
  crc:      datum.u16le


class RF24_AR_RadarMovement(datum.Datum):
  data:   datum.fp32(endian='little')


class RF24_AR_RadarPresence(datum.Datum):
  class PresenceState(enum.IntEnum):
    ABSENT  = 0x00FFFF
    STILL   = 0x0100FF
    ACTIVE  = 0x010101
  state:   datum.datum_bigint(size=3, signed=False, enum=PresenceState)


class RF24_AR_RadarDistance(datum.Datum):
  start:    datum.u8 = 0x01
  class DistanceState(enum.IntEnum):
    NO  = 1
    CLOSE   = 2
    FAR     = 3
  state: datum.u8(enum=DistanceState)


class RF24_SleepState(datum.Datum):
  class SleepState(enum.IntEnum):
    AWAKE   = 0
    LIGHT   = 1
    DEEP    = 2
    NO      = 3
  state: datum.u8(enum=SleepState)


class RF24_AR_RadarAbnormalReset(datum.Datum):
  start:    datum.u8 = 0x0F


class RF24_RespiratoryRate(datum.Datum):
  respitory_rate_pm: datum.u8


class RF24_RespitoryState(datum.Datum):
  class RespitoryState(enum.IntEnum):
    SUFFOCATION = 1
    NO = 2
    NORMAL = 3
    MOVEMENT = 4
    SHORTNESS = 5
  state: datum.u8(enum=RespitoryState)


class RF24_HeartRate(datum.Datum):
  heart_rate_bpm: datum.u8


FUNCTIONS = {
  0x040101: RF24_RespiratoryRate,
  0x040104: RF24_RespitoryState,
  0x040305: RF24_AR_RadarPresence,
  0x040306: RF24_AR_RadarMovement,
  0x040307: RF24_AR_RadarDistance,
  0x040601: RF24_HeartRate,
  0x040501: RF24_AR_RadarPresence,
  0x040502: RF24_AR_RadarAbnormalReset,
  0x050101: RF24_RespiratoryRate,
  0x050104: RF24_RespitoryState,
  0x050601: RF24_HeartRate,
  0x050308: RF24_SleepState,
}


class RadarR24B:
  def __init__(self, ser):
    self.ser = ser


  def poll(self):

    b = self.ser.read_all() # TODO impliment datum partial reads
    if not b: return

    try:
      r, more = R24Frame.deserialize_new(b)
      self.ser.push(more)
      payload, _ex = FUNCTIONS[r.command].deserialize_new(r.data)
      return payload
    except KeyError:
      LOG.exception(f'missing function {hex(r.command)}')
    except:
      LOG.debug(f'read {len(b)} bytes: {b.hex(' ')}')
      LOG.exception(f'Failed to parse. {b=}')
      raise


def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('port', type=str, default='COM13')
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

  ld = RadarR24B(ss)
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
# python -m devices.radar_ld2410 COM13

if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
  )
  main()
