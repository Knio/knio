#!/usr/bin/python3

import os
import sys
import pathlib
import threading

class Deleter:
  M = 2
  N = 1000
  def __init__(self):
    self.done = False
    self.queue = []
    self.qlock = threading.Lock()
    self.threads = []

  def extend(self, x):
    with self.qlock:
      self.queue.extend(x)

  def start(self):
    for _ in range(self.M):
      t = threading.Thread(target=self.run)
      self.threads.append(t)
      t.start()

  def run(self):
    while not self.done:
      with self.qlock:
        mine = self.queue[:self.N]
        self.queue[:self.N] = []
      if not mine:
        break

      for f in mine:
        self.process(f)

  def process(self, f):
    p = pathlib.Path(f)
    if not p.exists():
      print(f'missing {p}')
      return
    if p.is_dir():
      c = list(p.iterdir())
      if c:
        self.extend(c)
        self.extend([p])
      else: # empty dir
        print(f'rmdir {p}')
        # p.rmdir()
      return
    if p.is_file():
      print(f'unlink {p}')
      # p.unlink()
      return
    print(f'??? {p}')

  def wait(self):
    self.done = True
    for t in self.threads:
      t.join()
    self.threads[:] = []


def main():
  print('hello world')
  d = Deleter()
  d.extend(sys.argv[1:])
  d.start()
  d.wait()


if __name__ == '__main__':
  main()
