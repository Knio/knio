

import argparse
import logging
import time
import sqlite3
import json

import dominate
import whirl
from dominate import tags
from whirl.domx import dx


from collections import namedtuple

def namedtuple_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    cls = namedtuple("Row", fields)
    return cls._make(row)

conn = sqlite3.connect(
  'netflow.db',
)
conn.row_factory = namedtuple_factory

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

  tags.script(dominate.util.raw('''
    timeline = document.querySelector('#timeline');
    debug = document.querySelector('#debug');
    layout = {
      title: "network traffic",
      xaxis: {
        rangeslider: {}
      },
      yaxis: {
        fixedrange: true
      }
    };

    function update_zoom(data) {
      debug.innerText = JSON.stringify(data);
    }

  '''))

  tags.script(dominate.util.raw(f'''
    Plotly.newPlot(timeline, {json.dumps(graph)}, layout);
  '''))

  tags.script(dominate.util.raw('''
    time_range = [0,0];
    timeline.on('plotly_relayout',
    function(eventdata) {
        time_range = timeline.layout.xaxis.range.map(t => Math.floor(new Date(t).getTime()/1000));
        fetch("/domx/sumrange/" + time_range[0] + "/" + time_range[1]).then(response => {
          if (!response.ok) {
            debug.innerText = "response not ok";
            return;
          }
          response.json().then(data => {
            update_zoom(data);
          })
        })
    });

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

  args = parser.parse_args()


  whirl.domx.run(('', 8002))

if __name__ == '__main__':
  main()
