
import argparse
import logging
import time

import serial

from devices import utils

LOG = logging.getLogger(__name__)



def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('port', type=str, default='COM13')
  args = parser.parse_args()

  baud = 256000
  i = 0.9
  while i <= 1.1:
    i *= 1.01
    bb = int(baud * i)
    print(f'\nBaud: ({i:.3f}) {bb}')
    ser = serial.Serial(
      args.port,
      baudrate=bb,
      parity=serial.PARITY_NONE,
      bytesize=8,
      # stopbits=serial.STOPBITS_ONE_POINT_FIVE,
      # stopbits=serial.STOPBITS_TWO,
      stopbits=serial.STOPBITS_ONE,
      timeout=.2
    )
    ss = utils.PySerial(ser, timeout=1)

    # looking for:
    # f3f2 f10d 0002 aa03 3c00 3600 0064 0000 5500 f8f7 f6f5


    try:
      # print('### f4 f3f2 f10d 0002 aa03 3c00 3600 0064 0000 5500 f8f7 f6f5')
      for _ in range(20):
          data = ss.read()
          if b'\xf4\xf3\xf2\xf1' in data:
            print(f'--> {data.hex(" ", 2)}')

    except KeyboardInterrupt:
      pass

    ser.close()
    time.sleep(.4)

# to run: (from parent dir)
# python -m devices.test_serial COM13

if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
  )
  main()
