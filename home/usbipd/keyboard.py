#!/usr/bin/python3
'''

https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h


'''

import argparse
import sys
import pathlib
import enum
import datetime

bin = pathlib.Path(__file__).parent.parent.parent/'bin'
print(bin)
sys.path.append(str(bin))
print(sys.path)
import datum


class EvType(enum.IntEnum):
  EV_SYN = 0x00
  EV_KEY = 0x01
  EV_REL = 0x02
  EV_ABS = 0x03
  EV_MSC = 0x04
  EV_SW  = 0x05
  EV_LED = 0x11
  EV_SND = 0x12
  EV_REP = 0x14
  EV_FF  = 0x15
  EV_PWR = 0x16
  EV_FF_STATUS = 0x17
  EV_MAX = 0x1f


class EvMsc(enum.IntEnum):
  MSC_SERIAL    = 0x00
  MSC_PULSELED  = 0x01
  MSC_GESTURE   = 0x02
  MSC_RAW       = 0x03
  MSC_SCAN      = 0x04
  MSC_TIMESTAMP = 0x05
  MSC_MAX       = 0x07


class Timespec(datum.Datum):
  seconds: datum.u64(endian='native')
  microseconds: datum.u64(endian='native')
  def value(self):
    return datetime.datetime.fromtimestamp(
      self.seconds + (self.microseconds/1e6)
    )

class EVDev(datum.Datum):
  time: Timespec
  type: datum.u16(endian='native', enum=EvType)
  code: datum.u16(endian='native')
  value: datum.i32(endian='native')


def main():
  parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument('keyboard',
    nargs='?',
    type=pathlib.Path,
    default='/dev/input/by-id/usb-Pepper_Jobs_Limited_W11_GYRO-event-kbd'
  )
  args = parser.parse_args()


  kb = args.keyboard.open('rb', buffering=False)
  ev = EVDev()
  while 1:
    b = kb.read(ev.size())
    ev.deserialize_into(b)
    print(ev)


if __name__ == '__main__':
  main()
