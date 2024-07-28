import logging
import pathlib
import time
import toml

import requests

LOG = logging.getLogger(__name__)

CONF = toml.load(pathlib.Path(__file__).parent / 'config.toml')

config = CONF['grafana']

# https://grafana.com/docs/grafana-cloud/metrics-graphite/http-api/


def post_frame(data):
  auth = 'Bearer {}:{}'.format(59684, config['grafana_token'])
  now = int(time.time())
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



def post(ns, interval=2, **kv):
  auth = 'Bearer {}:{}'.format(59684, config['grafana_token'])
  now = int(time.time())
  data = [{
    'name': '.'.join((ns, k)),
    'value': v,
    'time': now,
    'interval': interval,
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
