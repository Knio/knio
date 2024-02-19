'''
run with:

 sudo python3 -m net.net

from the parent dir
'''

import datetime
import ipaddress
import logging
import pathlib
import collections
import time
import sqlite3
import argparse

from bcc import BPF

import grafana

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
  BPF.attach_xdp(dev=args['interface'], fn=b.load_func("peek_packet", BPF.XDP))
  flows = b["flows"]

  # b.trace_print()
  db = DB(args['db'])

  try:
    while 1:
      t = datetime.datetime.now()
      f = list(flows.items_lookup_and_delete_batch())

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

