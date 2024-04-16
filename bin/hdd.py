'''
Verify and benchmark a drive

'''

import argparse
import time
import logging


def main(args):
  f = open(args.file, 'wb')

  NB = 4 * 1024 * 1024
  buf = bytearray(NB)
  v = memoryview(buf)
  iv = v.cast('Q')
  NI = len(iv)
  count = 0

  times = []
  while 1:
    times.append(time.time())
    for i in range(NI):
      iv[i] = count + i
    count =+ NI
    f.write(buf)
    if len(times) > 2:
      dur = times[-1] - times[-2]
      speed = NB / dur
      print(f'{speed/1024/1024:.3f} MiB/s')


if __name__ == '__main__':
  logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(asctime)s %(name)s: %(message)s')
  parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument('file')
  args = parser.parse_args()
  main(args)
