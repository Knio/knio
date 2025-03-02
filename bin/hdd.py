'''
Verify and benchmark a drive

'''

import argparse
import time
import logging
import os
import random


KB = 1024
MB = KB**2
GB = KB**3


class DataGen:
  def __init__(self, size_mb=256):
    self.size = size_mb * MB
    self.rand_bytes_buf = os.urandom(self.size)
    self.rand_bytes = memoryview(self.rand_bytes_buf)
    self.zero_buf = bytearray(self.size)
    self.zero_bytes = memoryview(self.zero_buf)

  def get(self, n):
    x = random.randint(0, self.size - n)
    self.rand_bytes[x : x + n]

  def get_zero(self, n):
    return self.zero_bytes[0:n]


class DiskTester:
  def __init__(self) -> None:
    self.data = DataGen()

  def test_write(self, fd, bs):
    ts = time.perf_counter_ns()
    while 1:
      os.write(fd, self.data.get_zero(bs))
      os.fsync(fd)
      te = time.perf_counter_ns()
      yield te - ts
      ts = te


def main(args):
  dt = DiskTester()
  fd = os.open(args.file, 0
    | os.O_CREAT
    | os.O_BINARY
    | os.O_RDWR
    # | os.O_DIRECT # not on windows?
  )
  buffer_size = args.size * GB

  # TODO:
  # tui gui to use kb to pick from rand/seq read/write blocksize

  bs = 512
  while bs <= 32*MB:
    print(f'\n {bs} block size', flush=True)
    try:
      for dur in dt.test_write(fd, bs):
        bw = (bs / MB) / (dur / 1e9)
        print(f'{"\b"*100}{bw:7.3f} MB/s', end='', flush=True)

    except KeyboardInterrupt:
      pass
    bs <<= 1


if __name__ == '__main__':
  logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(asctime)s %(name)s: %(message)s')
  parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument('file')
  parser.add_argument('--size', '-s', type=int)
  args = parser.parse_args()
  main(args)
