import logging
import pathlib
import time
import toml

import requests

LOG = logging.getLogger(__name__)

CONF = toml.load(pathlib.Path(__file__).parent / 'config.toml')

config = CONF['grafana']
SESS = requests.sessions.Session()

# https://grafana.com/docs/grafana-cloud/metrics-graphite/http-api/


def post_frame(data):
  auth = 'Bearer {}:{}'.format(59684, config['grafana_token'])
  try:
    p = SESS.post(
      config['grafana_uri'],
      headers={'Authorization': auth, 'Content-Type':'application/json'},
      json=data,
      timeout=2,
    )
    p.raise_for_status()
    LOG.info(p.json())
  except Exception as e:
    LOG.error(e)
    LOG.error(data)


def fix_value(x):
  if isinstance(x, bool):
    if x is True:
      return 1
    if x is False:
      return 0
  if isinstance(x, (int, float)):
    return x
  raise ValueError(f'{type(x)} not supported by grafana (v={x!r})')

def post(ns, interval=2, **kv):
  now = int(time.time())
  data = [{
    'name': '.'.join((ns, k)),
    'value': fix_value(v),
    'time': now,
    'interval': interval,
  } for k,v in kv.items()]
  post_frame(data)
