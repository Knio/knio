'''
Run a webserver to show network flows
'''

import ipaddress
import argparse

import logging
import datetime
import json
import pathlib

import dominate
import whirl
from dominate import tags

from .db import FlowDB

LOG = logging.getLogger(__name__)
module_dir = pathlib.Path(__file__).parent
db = None

@whirl.domx.template
class dashboard(dominate.document):
  def __init__(self, *a, **kw):
    super(dashboard, self).__init__(*a, **kw)
    with self.head:
      tags.script(src="https://cdn.plot.ly/plotly-2.29.1.min.js")


@whirl.domx.route('/')
@tags.div
def index(url, handler):
  tags.h1('Hello world')

  tags.div(id="timeline")
  tags.div(id="details")
  tags.div(debug := tags.pre(id='debug'))

  with db as c:
    # TODO: compress time series (2000 buckets)
    c.execute('''
      SELECT
        time, bytes
      FROM
        flow
      WHERE
        ip_a is NULL
        AND ip_b is NULL
    ''')
    data = c.fetchall()

  with db as c:
    c.execute('''
      SELECT
        ip, json
      FROM
        ipapi
    ''')
    ipapi = [[x.ip, json.loads(x.json)] for x in c.fetchall()]


  graph = [dict(
    x=[x.time for x in data],
    y=[x.bytes for x in data]
  )]

  layout = dict(
    title = "network traffic",
    xaxis = dict(rangeslider = {}),
    yaxis = dict(fixedrange = True),
  )

  tags.script(dominate.util.raw(f'''
    var ipapi_raw = {json.dumps(ipapi)};
    Plotly.newPlot("timeline", {json.dumps(graph)}, {json.dumps(layout)});
  '''))
  topn(url, handler)

  tags.script(dominate.util.include(module_dir/'web.js'))

@whirl.domx.route('^/topn')
def topn(url, handler):
  with db as c:
    c.execute('''
      SELECT
        ip_a, SUM(bytes)
      FROM
        flow
      WHERE
        ip_b is NULL
        AND ip_a is not NULL
      GROUP BY
        ip_a
      ORDER BY
        SUM(bytes) DESC
      LIMIT 10
    ''')
    data = c.fetchall()
    c.execute('''
      SELECT
        ip_b, SUM(bytes)
      FROM
        flow
      WHERE
        ip_a is NULL
        AND ip_b is not NULL
      GROUP BY
        ip_b
      ORDER BY
        SUM(bytes) DESC
      LIMIT 10
    ''')
    data += c.fetchall()
  LOG.info(data)
  data.sort(key=lambda x: x.SUM_bytes_, reverse=True)
  with tags.table():
    for d in data:
      ip = d[0]
      tags.tr(
        tags.td(tags.input_(name='selected_ip', type='radio', value=f'{ip}')),
        tags.td(f'{ipaddress.ip_address(ip)}'),
        tags.td(f'{d.SUM_bytes_}'),
        id='topn'
      )
  return data

@whirl.domx.route('^/sumrange/(.+)/(.+)', type='json')
def sumrange(url, handler, start, end):
  start = datetime.datetime.fromtimestamp(int(start))
  end = datetime.datetime.fromtimestamp(int(end))
  LOG.info(f'sumrange: {start} -> {end}')
  with db as c:
    c.execute('''
      SELECT
        ip_a, ip_b, SUM(bytes)
      FROM
        flow
      WHERE
        time >= :start
        AND time <= :end
        AND ip_a is not NULL
        AND ip_b is not NULL
      GROUP BY
        ip_a, ip_b
    ''', locals())
    data = c.fetchall()
  return data


@whirl.domx.route('^/ipapi', type='json')
def ipapi(url, handler):
  with db as c:
    c.execute('''
      SELECT
        json
      FROM
        ipapi
    ''')
    data = c.fetchall()
  return data


def main():
  logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s')

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)
  parser.add_argument('--db', type=str, default='netflow.db')

  args = parser.parse_args()

  global db
  db = FlowDB(args.db)
  # db = FlowDB(f'file:{args.db}?mode=ro', uri=True)

  # ipapi.tick(db)
  whirl.domx.run(('', 8002))


if __name__ == '__main__':
  main()
