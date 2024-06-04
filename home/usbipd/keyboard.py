'''

'''

import argparse
import sys
import pathlib

bin = pathlib.Path(__file__).parent.parent.parent/'bin'
print(bin)
sys.path.append(str(bin))
print(sys.path)
import datum


class EVDev(datum.Datum):
  ts1: datum.uint64
  ts2: datum.uint64
  type: datum.uint16
  code: datum.uint16
  value: datum.uint32


def main():
  parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument('keyboard',
    type=pathlib.Path,
    default='/dev/input/by-id/usb-Pepper_Jobs_Limited_W11_GYRO-event-kbd'
  )
  args = parser.parse_args()


  kb = args.keyboard.open('rb', buffering=False)
  ev = EVDev()
  while 1:
    b = kb.read(ev.size())
    ev.deserialize(b)
    print(ev)


if __name__ == '__main__':
  main()
