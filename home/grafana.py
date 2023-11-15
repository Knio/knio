import logging
import pathlib
import time
import toml

import requests

LOG = logging.getLogger(__name__)

config = toml.load(pathlib.Path(__file__).parent / 'config.toml')['grafana']

# https://grafana.com/docs/grafana-cloud/metrics-graphite/http-api/

def post(ns, **kv):
  auth = 'Bearer {}:{}'.format(59684, config['grafana_token'])
  now = int(time.time())
  data = [{
    'name': '.'.join((ns, k)),
    'value': v,
    'time': now,
    'interval': 2,
  } for k,v in kv.items()]
  try:
    p = requests.post(
      config['grafana_uri'],
      headers={'Authorization': auth, 'Content-Type':'application/json'},
      json=data,
      timeout=2,
    )
    LOG.info(p.json())
  except Exception as e:
    LOG.error(e)
