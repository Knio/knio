import functools
import ipaddress
import logging
import pathlib
import time

from bcc import BPF


LOG = logging.getLogger('net.net')

import dataclasses
@dataclasses.dataclass
class Flow:
  src: ipaddress.IPv4Address
  dst: ipaddress.IPv4Address
  # TODO:
  # ipv6
  # protocol
  # srcport
  # dstport
  # num packets
  bytes: int


@functools.cache
def get_bpf():
  src_path = str(pathlib.Path(__file__).parent/'net.c')
  return BPF(src_file=src_path, debug=0)


def monitor(attachment, interface, printk=False):
  b = get_bpf()
  if attachment == 'socket':
    fn=b.load_func("sock_peek_packet", BPF.SOCKET_FILTER)
    BPF.attach_raw_socket(dev=interface, fn=fn)
  elif attachment == 'xdp':
    fn=b.load_func("xdp_peek_packet", BPF.XDP)
    BPF.attach_xdp(dev=interface, fn=fn)
  else:
    # TODO: tc (traffic control)
    raise ValueError(attachment)

  flows_hash = b["flows"]
  LOG.info('bpf ok')
  if printk:
    b.trace_print()

  try:
    while 1:
      flows = list(flows_hash.items_lookup_and_delete_batch())
      LOG.debug(f'{len(flows)} flows recoded')
      results = []
      for flow, stat in flows:
        a = ipaddress.ip_address(flow.ip_a)
        b = ipaddress.ip_address(flow.ip_b)
        f = Flow(b, a, stat)
        results.append(f)
        # debugging
        LOG.debug(f'{a} -> {b}: {stat}')
      yield results

  except KeyboardInterrupt:
    pass


if __name__ == '__main__':
  logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s')

  for data in monitor(attachment='socket', interface='eth0'):
    print(data)
    time.sleep(1)
