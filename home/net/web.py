'''
Run a webserver to show network flows
'''

import argparse
import logging
import time
import sqlite3
import json
import pathlib
from collections import namedtuple

import dominate
import whirl
from dominate import tags
from whirl.domx import dx


module_dir = pathlib.Path(__file__).parent
conn = None

def namedtuple_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    cls = namedtuple("Row", fields)
    return cls._make(row)


@whirl.domx.template
class dashboard(dominate.document):
  def __init__(self, *a, **kw):
    super(dashboard, self).__init__(*a, **kw)
    with self.head:
      tags.script(src="https://cdn.plot.ly/plotly-2.29.1.min.js")


@whirl.domx.route('/')
@tags.div
def index(url, handler, match):
  tags.h1('Hello world')

  tags.div(id="timeline")
  tags.div(debug := tags.pre(id='debug'))

  curs = conn.execute('''
    SELECT
      time, bytes
    FROM
      flow
    WHERE
      ip_a is NULL
      AND ip_b is NULL
  ''')
  data = curs.fetchall()

  graph = [dict(
    x=[x.time for x in data],
    y=[x.bytes for x in data]
  )]
  j = json.dumps(data, sort_keys=True, indent='  ')

  tags.script(dominate.util.include(module_dir/'net.js'))

  tags.script(dominate.util.raw(f'''
    Plotly.newPlot(timeline, {json.dumps(graph)}, layout);
  '''))

  tags.script(dominate.util.raw('''

  '''))


@whirl.domx.route('^/sumrange/(.+)/(.+)')
def sumrange(url, handler, match):
  start = int(match.group(1))
  end = int(match.group(2))
  curs = conn.execute('''
    SELECT
      ip_a, ip_b, SUM(bytes)
    FROM
      flow
    WHERE
      time >= :start
      AND time <= :end
    GROUP BY
      ip_a, ip_b
  ''', locals())
  data = curs.fetchall()
  return data
  # j = json.dumps(data, sort_keys=True, indent='  ')



def main():
  logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s')

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)
  parser.add_argument('--db', type=str, default='netflow.db')

  args = parser.parse_args()

  global conn
  conn = sqlite3.connect(args.db, readonly=True)
  conn.row_factory = namedtuple_factory


  whirl.domx.run(('', 8002))


if __name__ == '__main__':
  main()
