

def dep_check():
  import platform
  import pathlib
  import os
  import sys

  errors = []

  NAME = pathlib.Path(__file__).parent.name
  assert (r := platform.system()) == 'Linux', \
    f'{NAME} requires Linux. You have: {r}'

  pmaj, pmin, _ = platform.release().split('.', 2)
  if (int(pmaj), int(pmin)) < (5, 9):
    errors.append(f'{NAME} requires Linux kernel >= 5.9. You have: {r}')

  try:
    from bcc import BPF
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
    # exit(-1)

# dep_check()


import argparse
import dataclasses
import enum
import functools
import ipaddress
import logging
import os
import socket
import subprocess
import sys
import pathlib
import threading
import time

import blessed
import pandas
import bcc

from . import _version
from . import net
from . import utils

LOG = logging.getLogger('nettui')


# TODO port number tracking
# TODO print pretty bar graph
# TODO fast double buffered term library
# TODO lan rdns somehow
# TODO process (pid) tracking
# TODO hsz() coloring
# TODO tree of flows to expand host rollup to ports etc
# TODO root tree by pid, protocol, etc
# TODO mouse cursor
# TODO show extra data of selected
# TODO show time series graph of selected row


def get_local_ipv4_addresses():
  import fcntl
  import struct
  addrs = {}
  s4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
  for i, name in socket.if_nameindex():
    try:
      ip4 = socket.inet_ntoa(fcntl.ioctl(
          s4.fileno(),
          0x8915,  # SIOCGIFADDR
          struct.pack('256s', name[:15].encode('utf8'))
      )[20:24])
      addrs[ipaddress.IPv4Address(ip4)] = name
    except OSError:
      LOG.warning(f'Could not resolve IPv4 address for interface {name}')
  return addrs


def get_local_ipv6_addresses():
  tokens = map(
    str.split,
    pathlib.Path('/proc/net/if_inet6').read_text().splitlines()
  )
  return {ipaddress.IPv6Address(bytes.fromhex(t[0])): t[5] for t in tokens}


def get_local_addresses():
  v4 = get_local_ipv4_addresses()
  v6 = get_local_ipv6_addresses()
  v4.update(v6)
  return v6


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

@functools.total_ordering
class PrettyAddress:
  def __init__(self, addr):
    self.addr = addr

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

  @classmethod
  def type_key(cls, addr):
    if addr in LOCAL:        return cls.Type.LOCAL
    if addr.is_global:       return cls.Type.GLOBAL
    if addr.is_link_local:   return cls.Type.LINK_LOCAL
    if addr.is_loopback:     return cls.Type.LOOPBACK
    if addr.is_multicast:    return cls.Type.MULTICAST
    if addr.is_private:      return cls.Type.PRIVATE
    if addr.is_reserved:     return cls.Type.RESERVED
    if addr.is_unspecified:  return cls.Type.UNSPECIFIED
    return cls.Type.UNKNOWN

  @classmethod
  def _sort_key(cls, addr):
    return cls.type_key(addr), *ipaddress.get_mixed_type_key(addr)

  def sort_key(self):
    return type(self)._sort_key(self.addr)

  def __lt__(self, other):
    return (
      type(self)._sort_key(self.addr) <
      type(other)._sort_key(other.addr)
    )

  def __eq__(self, other):
    return (
      self.addr == other.addr
    )

  def __hash__(self):
    return hash(self.addr)

  def pretty(self):
    cls = type(self)
    c = {
      cls.Type.LOCAL: TERM.on_green,
      cls.Type.PRIVATE: TERM.orange,
      cls.Type.GLOBAL: TERM.cyan,
      cls.Type.MULTICAST: TERM.red,
    }.get(cls.type_key(self.addr), TERM.grey)
    s = DNS.resolve(self.addr)
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
    # some ui state
    self.pairs = []
    self.selected = None


  def run(self):
    # TODO reconfigure logging to not print to screen now
    print("press 'q' to quit.")
    with TERM.cbreak(), TERM.hidden_cursor(), TERM.fullscreen():
      while 1:
        print(TERM.home, end='')

        try:   val = TERM.inkey(timeout=self.interval)
        except KeyboardInterrupt: break

        if val.lower() == 'q':
          break

        # cursor
        elif val.is_sequence and val.name in ('KEY_UP', 'KEY_DOWN'):
          try:
            i = self.pairs.index(self.selected)
            i += 1 if val.name == 'KEY_DOWN' else -1
          except ValueError:
            i = 0
          try:
            self.selected = self.pairs[i]
          except IndexError:
            pass

        elif val.is_sequence:
          print("got sequence: {0}.".format((str(val), val.name, val.code)))
          time.sleep(1)

        elif val != '':
          print("got {0}.".format(val))
          time.sleep(1)

        # timeout
        elif val == '':
          self.update_flows()

        if not TERM.kbhit(0): # TODO not working
          self.draw_flows()

    print(f'{TERM.normal}bye!{TERM.clear_eol}')

  def update_flows(self):
    LOG.debug("update")
    for name, mon in self.mons.items():
      now = time.time()
      rows = []
      for flow in next(mon):
        d = dataclasses.asdict(flow)
        d['src'] = PrettyAddress(d['src'])
        d['dst'] = PrettyAddress(d['dst'])
        rows.append(d)
      if rows:
        df = pandas.DataFrame.from_records(rows, index=['src', 'dst'])
        df['timestamp'] = now
        self.log[now] = df

    if self.log:
      self.df = pandas.concat(self.log.values(), sort=False)
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

    grouped = window.groupby(level=['src', 'dst'],
      observed=True, sort=False)
    pairs = set()
    for pair in grouped.indices.keys():
      key = tuple(sorted(pair))
      pairs.add(key)

    def sort_key(x):
      a, b = x
      return PrettyAddress.sort_key(a) + PrettyAddress.sort_key(b)

    self.pairs = pairs = sorted(pairs, key=sort_key)

    # draw window
    W = TERM.width
    Hpad = 3 # could print one more line but has to make sure it doesn't end with \n
    H = TERM.height - Hpad

    try:
      k = self.pairs.index(self.selected)
    except ValueError:
      k = 0

    s = 0
    e = min(len(pairs), s + H)


    # print(TERM.move_xy(0, 1), end='')
    print(f'{TERM.black_on_white}    Network Flows past {dur}s {s+1}-{e} of {len(pairs)}{TERM.clear_eol}{TERM.normal}')
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

      P = 25
      src_s = TERM.ljust(src.pretty(), W // 2 - P)
      dst_s = TERM.rjust(dst.pretty(), W // 2 - P)
      if self.selected == (src, dst):
        sel = f'{TERM.RED}⮞'
      else:
        sel = f'{TERM.dim} '
      print(f'{sel}{i+s+1:3d}{TERM.normal}  {src_s} {tx_bytes:10,.0f} <--> {rx_bytes:10,.0f} {dst_s}{TERM.clear_eol}')
    print(f'{TERM.black_on_white}end{TERM.clear_eol}{TERM.normal}')

    for w in range(e - s, H):
      # visualize blank/available space
      print(TERM.normal + '>' + TERM.clear_eol)

    # TODO debug logs
    # print(TERM.clear)
    # print(TERM.move_xy(0, 40))


def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  # TODO these should be part of a config file
  parser.add_argument('--interfaces',
    '-i', nargs='*', type=str, default=())
  parser.add_argument('--interval',
    '-t', type=float, default=0.3)
  parser.add_argument('--attachment', '-a',
    type=str, default='socket')

  # internal args for escalation
  parser.add_argument('--escalated',
    help=argparse.SUPPRESS,
    default=False, action='store_true')

  print(f'bwninja version {_version.version} from {__file__} running as {os.getuid()}')

  args = parser.parse_args()

  if args.escalated and (os.getuid() == 0):
    print('sudo successful')

  # run as user. needs upgrade
  if (not args.escalated) and (os.getuid() != 0):
    print('root required, attempting to sudo..')
    paths = utils.get_import_paths(utils, blessed, bcc, pandas)
    utils.escalate(paths, '--escalated')

  del args.escalated

  NetTui(**vars(args)).run()


if __name__ == '__main__':
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s')

  main()
