

def dep_check():
  import platform
  import pathlib
  import os
  import sys

  errors = []

  NAME = pathlib.Path(__file__).parent.name
  assert (r := platform.system()) == 'Linux', \
    f'{NAME} requires Linux. You have: {r}'

  if (r := platform.release()) < '5.9':
    errors.append(f'{NAME} requires Linux kernel >= 5.9. You have: {r}')

  try:
    import bcc
  except ImportError:
    errors.append(
        f'{NAME} requires python3-bpfcc which may not be satisfiable from pip. \n'
        '    See: https://github.com/iovisor/bcc/blob/master/INSTALL.md')

  if os.getuid() != 0:
    errors.append(f'{NAME} must be run as root')

  try:
    from . import net
  except ImportError as e:
    errors.append(
      f'Could not import required {NAME} module. ({e})\n'
      '    Did you perhaps install to a venv or user-install location, but then run it as root?\n'
      '    Unfortunately, it will have to be installed as root.\n'
      '    Try:\n'
      f'        sudo -H python3 -m pip install {NAME} --break-system-packages')

  if errors:
    errs = "\n\n".join(errors)
    print(f'Unable to run. please correct the following errors:\n\n{errs}', file=sys.stderr)
    exit(-1)

dep_check()


import argparse
import dataclasses
import enum
import ipaddress
import logging
import socket
import threading
import time

import blessed
import pandas

from . import net

LOG = logging.getLogger('nettui')

# TODO print pretty bar graph
# TODO lan rdns somehow
# TODO process (pid) tracking
# TODO hsz() coloring
# TODO cursor
# TODO ipv6 support
# TODO tree of flows to expand host rollup to ports etc
# TODO root tree by pid, protocol, etc
# TODO mouse cursor
# TODO show extra data of selected
# TODO show time series graph of selected row


dep_check()

def get_local_addresses():
  import fcntl
  import struct
  addrs = {}
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  for i, name in socket.if_nameindex():
    try:
      ip = socket.inet_ntoa(fcntl.ioctl(
          s.fileno(),
          0x8915,  # SIOCGIFADDR
          struct.pack('256s', name[:15].encode('utf8'))
      )[20:24])
      addrs[ipaddress.IPv4Address(ip)] = name
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
    except KeyError: pass

    if key in LOCAL:
      s = f'[{HOST}.{LOCAL[key]}] {key}'
      self.resolved[key] = s
      return s

    self.pending.add(key)
    self.event.set()

    return str(key) # TODO coloring


TERM = blessed.Terminal()
TERM.number_of_colors = 256
DNS = DNSCache()
HOST = socket.gethostname()
LOCAL = get_local_addresses()

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


  def type_key(self):
    if self in LOCAL:        return Address.Type.LOCAL
    if self.is_global:       return Address.Type.GLOBAL
    if self.is_link_local:   return Address.Type.LINK_LOCAL
    if self.is_loopback:     return Address.Type.LOOPBACK
    if self.is_multicast:    return Address.Type.MULTICAST
    if self.is_private:      return Address.Type.PRIVATE
    if self.is_reserved:     return Address.Type.RESERVED
    if self.is_unspecified:  return Address.Type.UNSPECIFIED
    return Address.Type.UNKNOWN

  def sort_key(self):
    return self.type_key(), self

  def pretty(self):
    c = {
      Address.Type.LOCAL: TERM.on_green,
      Address.Type.PRIVATE: TERM.orange,
      Address.Type.GLOBAL: TERM.cyan,
      Address.Type.MULTICAST: TERM.red,
    }.get(self.type_key(), TERM.grey)
    s = DNS.resolve(self)
    return c + s + TERM.normal

class Stats:
  def __init__(self, ser):
    self.ser = ser

  @property
  def duration(self):
    ts = self.ser['timestamp']
    return max(1, ts.max() - ts.min())

  @property
  def mean_bytes(self):
    return self.ser['bytes'].sum() / self.duration

class NetTui:
  def __init__(self, interval, interfaces, **kw):
    self.interval = interval
    self.dns = DNSCache()
    if not interfaces:
      interfaces = list(LOCAL.values())
    self.mons = {dev: net.monitor(interface=dev, **kw) for dev in interfaces}
    [next(m) for m in self.mons.values()]
    self.df = pandas.DataFrame()
    self.log = {}
    self.history = 600


  def run(self):
    # TODO reconfigure logging to not print to screen now
    print("press 'q' to quit.")
    with TERM.cbreak(), TERM.hidden_cursor(), TERM.fullscreen():
      while 1:
        self.update_flows()
        print(TERM.home, end='')
        # print(TERM.home + TERM.clear, end='')

        self.draw_flows()
        try:   val = TERM.inkey(timeout=self.interval)
        except KeyboardInterrupt: break

        # timeout
        if val == '': continue

        if val.is_sequence:
          print("got sequence: {0}.".format((str(val), val.name, val.code)))
          continue

        print("got {0}.".format(val))
        if val.lower() == 'q': break
    print(f'bye!{TERM.normal}')

  def update_flows(self):
    # LOG.debug("update")

    for name, mon in self.mons.items():
      now = time.time()
      rows = []
      for flow in next(mon):
        d = dataclasses.asdict(flow)
        d['src'] = Address(d['src'].packed)
        d['dst'] = Address(d['dst'].packed)
        rows.append(d)
      if rows:
        df = pandas.DataFrame.from_records(rows, index=['src', 'dst'])
        df['timestamp'] = now
        self.log[now] = df

    if self.log:
      self.df = pandas.concat(self.log.values())
    for ts in list(self.log.keys()):
      if ts + self.history < now:
        del self.log[ts]


  def draw_flows(self):
    now = time.time()
    dur = 30
    since = now - dur

    if len(self.df) == 0: return
    window = self.df.loc[self.df['timestamp'] > since]
    if len(window) == 0: return

    grouped = window.groupby(level=['src', 'dst'], observed=True)
    pairs = set()
    for pair in grouped.indices.keys():
      key = tuple(sorted(pair, key=Address.sort_key))
      pairs.add(key)

    def sort_key(x):
      a, b = x
      return Address.sort_key(a) + Address.sort_key(b)

    pairs = sorted(pairs, key=sort_key)

    W = TERM.width

    s = 0
    e = len(pairs)
    # print(TERM.move_xy(0, 1), end='')
    print(f'{TERM.black_on_white}    Network Flows past {dur}s {s+1}-{len(pairs)}{TERM.clear_eol}{TERM.normal}')
    for i, (src, dst) in enumerate(pairs[s:e]):
      try:
        tx = grouped.get_group((src, dst))
        tx_bytes = Stats(tx).mean_bytes
      except KeyError:
        tx_bytes = 0
      try:
        rx = grouped.get_group((dst, src))
        rx_bytes = Stats(rx).mean_bytes
      except KeyError:
        rx_bytes = 0

      P = 24
      src_s = TERM.ljust(src.pretty(), W // 2 - P)
      dst_s = TERM.rjust(dst.pretty(), W // 2 - P)
      print(f'{TERM.dim}{i+s+1:3d}{TERM.normal}  {src_s} {tx_bytes:10,.0f} <--> {rx_bytes:10,.0f} {dst_s}{TERM.clear_eol}')
    print(f'{TERM.black_on_white}end{TERM.clear_eol}{TERM.normal}')

    for w in range(e - s + 3, TERM.height):
      print(TERM.normal + '>' + TERM.clear_eol)

    # TODO debug logs
    # print(TERM.clear)
    # print(TERM.move_xy(0, 40))


def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('--interfaces', '-i', nargs='*', type=str, default=())
  parser.add_argument('--interval', '-t', type=float, default=0.3)
  parser.add_argument('--attachment', '-a', type=str, default='socket')
  parser.add_argument('--printk', default=False, action='store_true')

  args = parser.parse_args()
  NetTui(**vars(args)).run()


if __name__ == '__main__':
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s')

  main()
