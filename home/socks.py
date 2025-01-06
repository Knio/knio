#! /usr/bin/python3

import logging
import os
import signal
import subprocess
import threading
import time


LOG = logging.getLogger(__name__)


class SocksServer:
  def __init__(self, host: str):
    self.host = host
    self.ssh = None


  def run(self):
    while 1:
      if not self.ssh:
        time.sleep(10)
        try:
          self.reset()
        except:
          LOG.exception('Failed to reset')
          continue
      line = self.ssh.stderr.readline()
      try:
        line = line.decode('utf8').strip()
      except UnicodeDecodeError:
        pass
      LOG.info(f'{self.host}:{line}')
      r = self.ssh.poll()
      if r is not None:
        LOG.info(f'exit {r} from pid:{self.ssh.pid}')
        self.ssh = None


  def start(self):
    self.thread = threading.Thread(target=self.run)
    self.thread.start()


  def reset(self):
    self.stop()
    self.ssh = subprocess.Popen(cmd := ['ssh',
      '-N', '-n', '-v', '-T',
      '-o', 'PasswordAuthentication=false',
      '-R', '19443', self.host,
    ], stdin=subprocess.DEVNULL, stderr=subprocess.PIPE)
    LOG.info(f'started pid:{self.ssh.pid} {" ".join(cmd)}')


  def stop(self):
    if self.ssh:
      LOG.info(f'{self.host} sending {self.ssh.pid} SIGINT')
      self.ssh.send_signal(sig=signal.SIGINT)
      try:
        self.ssh.wait(10)
      except subprocess.TimeoutExpired:
        LOG.info(f'{self.host} sending {self.ssh.pid} SIGINT')
        self.ssh.send_signal(sig=signal.SIGTERM)
      try:
        self.ssh.wait(10)
      except subprocess.TimeoutExpired:
        LOG.info(f'{self.host} sending {self.ssh.pid} SIGKILL')
        self.ssh.kill()
        self.ssh.wait()
    self.ssh = None


def main():
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s %(message)s')

  SocksServer('zkpq.ca').start()
  SocksServer('dfg.hjkl.ca').start()
  SocksServer('cvb.hjkl.ca').start()

if __name__ == '__main__':
  main()
