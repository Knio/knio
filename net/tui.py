import argparse
import dataclasses
import logging
import socket
import threading
import time

import blessed
import pandas

import net

LOG = logging.getLogger('nettui')

# TODO print pretty bar graph
# TODO IP/hostname coloring
# TODO process (pid) tracking
# TODO hsz() coloring
# TODO cursor
# TODO tree of flows to expand host rollup to ports etc
# TODO root tree by pid, protocol, etc
# TODO mouse cursor
# TODO show time series of selected


class DNSCache(dict):
  def __init__(self):
    super().__init__(self)
    self.pending = set()
    self.event = threading.Event()
    self.thread = threading.Thread(target=self.run)
    self.thread.daemon = True
    self.thread.start()

  def run(self):
    while 1:
      self.event.wait(timeout=10)
      self.event.clear()
      for ip in list(self.pending):
        try:
          hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(str(ip))
          self[ip] = hostname
          self.pending.remove(ip)
        except socket.herror as e:
          if e.errno == 1:
            self[ip] = f'{ip} ?' # TODO use some coloring
            self.pending.remove(ip)

  def __getitem__(self, key):
    try:
      return super().__getitem__(key)
    except KeyError:
      self.pending.add(key)
      self.event.set()
      return key # TODO coloring


class NetTui:
  def __init__(self, interval, **kw):
    self.interval = interval
    self.dns = DNSCache()
    self.mon = net.monitor(**kw)
    next(self.mon)
    self.term = blessed.Terminal()
    self.df = pandas.DataFrame()
    self.log = {}


  def run(self):
    term = self.term
    # TODO reconfigure logging to not print to screen now
    print(self.term.enter_fullscreen())
    print(f"{term.home}{term.black_on_skyblue}{term.clear}")
    print("press 'q' to quit.")
    with term.cbreak():
        while 1:
            self.update_flows()
            self.draw_flows()
            try:
              val = term.inkey(timeout=self.interval)
            except KeyboardInterrupt:
              break

            # timeout
            if val == '':
              continue

            if val.is_sequence:
              print("got sequence: {0}.".format((str(val), val.name, val.code)))
              continue

            print("got {0}.".format(val))
            if val.lower() == 'q':
              break


    print(f'bye!{term.normal}')
    print(self.term.exit_fullscreen())

  def update_flows(self):
    LOG.debug("update")
    now = time.time()
    rows = next(self.mon)
    df = pandas.DataFrame.from_records(map(dataclasses.asdict, rows), index=['src', 'dst'])
    df['timestamp'] = now

    self.log[now] = df
    self.df = pandas.concat(self.log.values())


  def draw_flows(self):
    now = time.time()
    since = now - 30
    window = self.df.loc[self.df['timestamp'] > since]


    grouped = window.groupby(level=['src', 'dst'])
    pairs = set()
    for pair in grouped.indices.keys():
      # TODO sort "local" IPs first so they're always on the left
      key = tuple(sorted(pair))
      pairs.add(key)

    # TODO sort pairs
    W = self.term.width

    print(self.term.move_xy(0, 1))
    for (src, dst) in pairs:
      try:
        tx = grouped.get_group((src, dst))
        tx_bytes = tx['bytes'].mean()
      except KeyError:
        tx_bytes = 0
      try:
        rx = grouped.get_group((dst, src))
        rx_bytes = rx['bytes'].mean()
      except KeyError:
        rx_bytes = 0




      src_s = self.dns[src]
      dst_s = self.dns[dst]
      print(f'{src_s:16s} {tx_bytes:8,.0f} <--> {rx_bytes:8,.0f}    {dst_s:>16s}{self.term.clear_eol}')

    # hack for debug logs
    print(self.term.move_xy(0, 40))


def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('--interface', '-i', type=str, default='eth0')
  parser.add_argument('--interval', '-t', type=float, default=0.5)
  parser.add_argument('--attachment', '-a', type=str, default='socket')
  parser.add_argument('--printk', default=False, action='store_true')

  args = parser.parse_args()
  NetTui(**vars(args)).run()


if __name__ == '__main__':
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s')

  main()
