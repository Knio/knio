import json
import ipaddress
import time
import collections
import argparse
import datetime
import requests
import logging

from .db import FlowDB

LOG = logging.getLogger(__name__)

def tick(db):
  # TODO: add all prefix subnets of ips

  ips = collections.defaultdict(int)
  with db as c:
    c.execute('''
      SELECT ip_a, SUM(bytes)
      FROM flow
      WHERE
        ip_a is not NULL
        AND ip_a NOT IN (SELECT ip FROM ipapi)
      GROUP BY ip_a
      ORDER BY SUM(bytes) DESC
      LIMIT 100
    ''')
    for row in c.fetchall():
      ips[row.ip_a] += row.SUM_bytes_
    c.execute('''
      SELECT ip_b, SUM(bytes)
      FROM flow
      WHERE
        ip_b is not NULL
        AND ip_b NOT IN (SELECT ip FROM ipapi)
      GROUP BY ip_b
      ORDER BY SUM(bytes) DESC
      LIMIT 100
    ''')
    for row in c.fetchall():
      ips[row.ip_b] += row.SUM_bytes_

  ips = sorted(ips.items(), key=lambda x: x[1], reverse=True)

  if not ips:
    return

  query = [
    str(ipaddress.ip_address(ip[0])) for ip in ips[:100]
  ]
  t = datetime.datetime.now()
  r = requests.post('http://ip-api.com/batch', json=query, timeout=15)
  r.raise_for_status()
  inserts = []
  for response in r.json():
    if response['status'] != 'success':
      LOG.error(response)
    ip = int(ipaddress.ip_address(response['query']))
    j = json.dumps(response, sort_keys=True, indent=2)
    LOG.info(response)
    inserts.append((t, ip, j))

  with db as c:
    c.executemany(
      '''
        INSERT INTO ipapi (time, ip, json)
        VALUES (?, ?, ?);
      ''',
      inserts
    )
  return


def main():
  logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s')

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)
  parser.add_argument('--db', type=str, default='netflow.db')

  args = parser.parse_args()

  db = FlowDB(args.db)
  while 1:
    time.sleep(2)
    tick(db)


if __name__ == '__main__':
  main()
