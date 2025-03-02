'''
run with:

 sudo python3 -m net.net

from the parent dir


CONFIG NOTES:

MTU + overhead must fit in one page:

 sudo ifconfig ens5 mtu 3000

sudo ethtool -l ens5
sudo ethtool -L ens5 combined 1

'''

import datetime
import ipaddress
import logging
import argparse

import pathlib
import collections
import time

from bcc import BPF
from db import FlowDB


LOG = logging.getLogger('net')


def run(args):
  src_path = str(pathlib.Path(__file__).parent/"net.c")
  b = BPF(src_file=src_path, debug=0)

  if args['attachment'] == 'socket':
    fn=b.load_func("sock_peek_packet", BPF.SOCKET_FILTER)
    BPF.attach_raw_socket(dev=args['interface'], fn=fn)
  elif args['attachment'] == 'xdp':
    fn=b.load_func("xdp_peek_packet", BPF.XDP)
    BPF.attach_xdp(dev=args['interface'], fn=fn)
  else:
    # TODO: tc (traffic control)
    raise ValueError(args['attachment'])

  flows = b["flows"]
  LOG.info('bpf ok')
  if args['printk']:
    b.trace_print()
  db = FlowDB(args['db'])

  try:
    while 1:
      t = datetime.datetime.now()
      f = list(flows.items_lookup_and_delete_batch())
      LOG.debug(f'{len(f)} flows recoded')
      inserts = []
      host_src = collections.defaultdict(int)
      host_dst = collections.defaultdict(int)
      total = 0
      for flow, stat in f:
        inserts.append((t, flow.ip_a, flow.ip_b, stat))
        host_src[flow.ip_a] += stat
        host_dst[flow.ip_b] += stat
        total += stat
        # debugging
        a = ipaddress.ip_address(flow.ip_a)
        b = ipaddress.ip_address(flow.ip_b)
        print(f'{a} -> {b}: {stat}')

      for ip_a, stat in host_src.items():
        inserts.append((t, ip_a, None, stat))
      for ip_b, stat in host_dst.items():
        inserts.append((t, None, ip_b, stat))
      inserts.append((t, None, None, total))


      with db as c:
        c.executemany(
          '''
            INSERT INTO flow (time, ip_a, ip_b, bytes)
            VALUES (?, ?, ?, ?);
          ''',
          inserts
        )

      time.sleep(args['interval'])

  except KeyboardInterrupt:
    pass


def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('--interface', '-i', type=str, default='eth0')
  parser.add_argument('--interval', '-t', type=int, default=5)
  parser.add_argument('--attachment', '-a', type=str, default='socket')
  parser.add_argument('--db', type=str, default='netflow.db')
  parser.add_argument('--printk', default=False, action='store_true')

  args = parser.parse_args()
  run(vars(args))


if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s')

  main()
