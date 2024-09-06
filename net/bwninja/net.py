import functools
import ipaddress
import logging
import pathlib
import time
import os

import bcc

from . import utils


LOG = logging.getLogger('net.net')

import dataclasses
@dataclasses.dataclass
class Flow:
  src: ipaddress.IPv4Address
  dst: ipaddress.IPv4Address
  protocol: int
  sport: int
  dport: int
  # payload
  packets: int
  bytes: int


@functools.cache
def get_bpf():
  # sanity warning
  try:
    assert 1 == int(pathlib.Path('/proc/sys/net/core/bpf_jit_enable').read_text())
  except Exception as e:
    LOG.warning(f'eBPF JIT is not enabled. This could slow performance. ({e!r})')
  src_path = str(pathlib.Path(__file__).parent / 'net.c')
  LOG.info(f'compiling bpf code from {src_path}')
  return bcc.BPF(src_file=src_path, debug=0)


def monitor(attachment, interface, printk=False):
  b = get_bpf()
  sfs = pathlib.Path(f'/sys/class/net/{interface}')
  addr_len = int((sfs / 'addr_len').read_text())
  if addr_len == 6:
    # assume this is ethernet
    fn=b.load_func('sock_peek_packet_eth', bcc.BPF.SOCKET_FILTER)
  elif addr_len == 0:
    fn=b.load_func('sock_peek_packet_ip', bcc.BPF.SOCKET_FILTER)
  else:
    raise ValueError(f'Unknown addr_len: {addr_len}')

  if attachment == 'socket':
    bcc.BPF.attach_raw_socket(dev=interface, fn=fn)
  elif attachment == 'xdp':
    fn=b.load_func('xdp_peek_packet', bcc.BPF.XDP)
    bc.BPF.attach_xdp(dev=interface, fn=fn)
  else:
    # TODO: tc (traffic control)
    raise ValueError(attachment)

  flows4_hash = b['flows4']
  flows6_hash = b['flows6']
  LOG.info('bpf attached')

  if printk:
    b.trace_print()

  try:
    while 1:
      flows4 = list(flows4_hash.items_lookup_and_delete_batch())
      LOG.debug(f'{len(flows4)} flows4 recoded')
      results = []
      for flow, stat in flows4:
        a = ipaddress.ip_address(flow.src)
        b = ipaddress.ip_address(flow.dst)
        LOG.debug(f'{a} -> {b}: {stat}')
        f = Flow(a, b, flow.ports.protocol, flow.ports.sport, flow.ports.dport, stat.packets, stat.bytes)
        results.append(f)

      flows6 = list(flows6_hash.items_lookup_and_delete_batch())
      LOG.debug(f'{len(flows6)} flows6 recoded')
      for flow, stat in flows6:
        a = ipaddress.ip_address(bytes(flow.src))
        b = ipaddress.ip_address(bytes(flow.dst))
        LOG.debug(f'{a} -> {b}: {stat}')
        f = Flow(a, b, flow.ports.protocol, flow.ports.sport, flow.ports.dport, stat.packets, stat.bytes)
        results.append(f)

      yield results

  except KeyboardInterrupt:
    pass


if __name__ == '__main__':
  logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s')

  import argparse
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('--interface',
    '-i', type=str, default='eth0')
  parser.add_argument('--attachment', '-a',
    type=str, default='socket')
  parser.add_argument('--printk', '-k',
    default=False, action='store_true')

  args = parser.parse_args()

  # run as user. needs upgrade
  if os.getuid() != 0:
    print('root required, attempting to sudo..')
    paths = utils.get_import_paths(utils, bcc)
    utils.escalate(paths)


  for data in monitor(**vars(args)):
    print(data)
    time.sleep(1)
