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
import pathlib
import collections
import time
import sqlite3
import argparse
import subprocess

from bcc import BPF

# import grafana

LOG = logging.getLogger('net')


class DB:
  def __init__(self, filename):
    self.conn = sqlite3.connect(filename)
    with self as c:
      c.execute('''
        CREATE TABLE IF NOT EXISTS flow (
          time DATETIME,
          ip_a INTEGER,
          ip_b INTEGER,
          bytes INTEGER
        );
      ''')
      c.execute('CREATE INDEX IF NOT EXISTS index_time ON flow (time);')
      c.execute('CREATE INDEX IF NOT EXISTS index_ip_a ON flow (ip_a);')
      c.execute('CREATE INDEX IF NOT EXISTS index_ip_b ON flow (ip_b);')
      c.execute('CREATE INDEX IF NOT EXISTS index_t_ip_a ON flow (time, ip_a);')
      c.execute('CREATE INDEX IF NOT EXISTS index_t_ip_b ON flow (time, ip_b);')
      LOG.info('database ok')

  def close(self):
    self.conn.commit()
    self.conn.close()

  def __enter__(self):
    return self.conn.cursor()

  def __exit__(self, et, ev, tb):
    if ev is None:
      self.conn.commit()
    else:
      self.conn.rollback()

def run(args):

  src_path = str(pathlib.Path(__file__).parent/"net.c")
  b = BPF(src_file=src_path, debug=0)
  fn=b.load_func("tc_peek_packet", BPF.SCHED_CLS)
  # fn=b.load_func("xdp_peek_packet", BPF.XDP)
  # BPF.attach_xdp(
  #   dev=args['interface'],
  #   fn=fn
  # )


'''
ifc = ipdb.interfaces.eth0

ipr.tc("add", "ingress", ifc.index, "ffff:")
ipr.tc("add-filter", "bpf", ifc.index, ":1", fd=ingress_fn.fd,
       name=ingress_fn.name, parent="ffff:", action="ok", classid=1)
ipr.tc("add", "sfq", ifc.index, "1:")
ipr.tc("add-filter", "bpf", ifc.index, ":1", fd=egress_fn.fd,
       name=egress_fn.name, parent="1:", action="ok", classid=1)

'''

  # sudo tc qdisc add dev wg0 parent root pfifo
  # sudo tc filter add dev wg0 parent root handle :1234 filtertype bpf name tc_peek_packet fd /dev/fd/NNN

  subprocess.check_output([
    'tc',
    'filter', 'add',
    'dev', 'wg0',
    'parent', 'root',
    'handle', ':1234',
    'filtertype', 'bpf',
    'name', fn.name,
    'fd', str(fn.fd),
  ])

  flows = b["flows"]
  LOG.info('bpf ok')
  # b.trace_print()
  db = DB(args['db'])

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
      for ip_b, stat in host_src.items():
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

