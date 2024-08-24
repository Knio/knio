import ipaddress
import argparse
import dataclasses
import logging
import socket
import threading
import time
import enum

import blessed
import pandas

import net

LOG = logging.getLogger('nettui')

# TODO print pretty bar graph
# TODO IP/hostname coloring
# TODO attach to multiple interfaces
# TODO process (pid) tracking
# TODO hsz() coloring
# TODO cursor
# TODO ipv6 support
# TODO tree of flows to expand host rollup to ports etc
# TODO root tree by pid, protocol, etc
# TODO mouse cursor
# TODO show time series of selected


import socket
import fcntl
import struct


def get_local_addresses():
    addrs = set()
    for i, name in socket.if_nameindex():
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      try:
        ip = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', name[:15].encode('utf8'))
        )[20:24])
        addrs.add(ipaddress.IPv4Address(ip))
      except OSError:
        LOG.warning(f'Could not resolve address for interface {name}')
    return addrs


class DNSCache:
  def __init__(self):
    self.resolved = {}
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
          self.resolved[ip] = hostname
          self.pending.remove(ip)
        except socket.herror as e:
          if e.errno == 1:
            self.resolved[ip] = f'{ip} ?' # TODO use some coloring
            self.pending.remove(ip)

  def resolve(self, key):
    try:
      return self.resolved[key]
    except KeyError:
      self.pending.add(key)
      self.event.set()
      return str(key) # TODO coloring

DNS = DNSCache()
TERM = blessed.Terminal()
TERM.number_of_colors = 256

class Address(ipaddress.IPv4Address):
  # TODO IPv6
  class Type(enum.IntEnum):
    LOCAL       = enum.auto()
    UNKNOWN     = enum.auto()
    LINK_LOCAL  = enum.auto()
    LOOPBACK    = enum.auto()
    MULTICAST   = enum.auto()
    PRIVATE     = enum.auto()
    RESERVED    = enum.auto()
    UNSPECIFIED = enum.auto()
    GLOBAL      = enum.auto()

  LOCAL = get_local_addresses()

  def type_key(self):
    if self in Address.LOCAL: return Address.Type.LOCAL
    if self.is_global:      return Address.Type.GLOBAL
    if self.is_link_local:  return Address.Type.LINK_LOCAL
    if self.is_loopback:    return Address.Type.LOOPBACK
    if self.is_multicast:   return Address.Type.MULTICAST
    if self.is_private:     return Address.Type.PRIVATE
    if self.is_reserved:    return Address.Type.RESERVED
    if self.is_unspecified: return Address.Type.UNSPECIFIED
    return Address.Type.UNKNOWN

  def sort_key(self):
    return self.type_key(), self

  def pretty(self):
    c = {
      Address.Type.LOCAL: TERM.green + TERM.bold,
      Address.Type.PRIVATE: TERM.orange,
      Address.Type.GLOBAL: TERM.cyan,
      Address.Type.MULTICAST: TERM.red,
    }.get(self.type_key(), TERM.grey)
    s = DNS.resolve(self)
    return c + s + TERM.normal



class NetTui:
  def __init__(self, interval, **kw):
    self.interval = interval
    self.dns = DNSCache()
    self.mon = net.monitor(**kw)
    next(self.mon)
    self.df = pandas.DataFrame()
    self.log = {}
    self.history = 600


  def run(self):
    # TODO reconfigure logging to not print to screen now
    print(TERM.enter_fullscreen())
    print(f"{TERM.home}{TERM.black_on_skyblue}{TERM.clear}")
    print("press 'q' to quit.")
    with TERM.cbreak():
        while 1:
            self.update_flows()
            self.draw_flows()
            try:
              val = TERM.inkey(timeout=self.interval)
            except KeyboardInterrupt: break

            # timeout
            if val == '': continue

            if val.is_sequence:
              print("got sequence: {0}.".format((str(val), val.name, val.code)))
              continue

            print("got {0}.".format(val))
            if val.lower() == 'q': break


    print(f'bye!{TERM.normal}')
    print(TERM.exit_fullscreen())

  def update_flows(self):
    LOG.debug("update")
    now = time.time()
    rows = []
    for flow in next(self.mon):
      d = dataclasses.asdict(flow)
      d['src'] = Address(d['src'].packed)
      d['dst'] = Address(d['dst'].packed)
      rows.append(d)
    df = pandas.DataFrame.from_records(rows, index=['src', 'dst'])
    df['timestamp'] = now
    self.log[now] = df
    self.df = pandas.concat(self.log.values())

    for ts in sorted(self.log.keys()):
      if ts + self.history < now:
        del self.log[ts]


  def draw_flows(self):
    TERM = TERM
    now = time.time()
    since = now - 30
    window = self.df.loc[self.df['timestamp'] > since]


    grouped = window.groupby(level=['src', 'dst'])
    pairs = set()
    for pair in grouped.indices.keys():
      # TODO sort "local" IPs first so they're always on the left
      key = tuple(sorted(pair, key=Address.sort_key))
      pairs.add(key)

    def sort_key(x):
      a, b = x
      return Address.sort_key(a) + Address.sort_key(b)
    pairs = sorted(pairs, key=sort_key)

    W = TERM.width

    print(TERM.move_xy(0, 1))
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

      P = 24
      src_s = TERM.ljust(src.pretty(), W // 2 - P)
      dst_s = TERM.rjust(dst.pretty(), W // 2 - P)
      print(f'{src_s} {tx_bytes:8,.0f} <--> {rx_bytes:8,.0f} {dst_s}{TERM.clear_eol}')

    # hack for debug logs
    # print(TERM.clear)
    print(TERM.move_xy(0, 40))


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
