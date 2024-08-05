import argparse
import logging
import toml
import pathlib

import grafana

from devices import kasa

LOG = logging.getLogger('air')

config = toml.load(pathlib.Path(__file__).parent / 'config.toml')['kasa']


def main(args):

  #pylint: disable=import-outside-toplevel
  if args.discover:
    dev = kasa.discover(
      '10.87.1.41',
    )
    # print(dev)
    print(dev.config.to_dict())
    return

  plugs = [
      # TODO try add
      kasa.Synced(kasa.discover('10.87.1.41', **config)),
      kasa.Synced(kasa.discover('10.87.1.42', **config)),
      kasa.Synced(kasa.discover('10.87.1.43', **config)),
      # kasa_light.Synced(kasa_light.discover('10.87.1.44', **config)),
  ]
  for p in plugs:
    p.update()
    print(p.dev.config.to_dict())
    print(p.dev.modules)
    print(type(p.dev))
    # print(p.dev)

  while 1:
    r = {}
    for i, p in enumerate(plugs):
      try:
        p.update()
        e = p.dev.emeter_realtime
      except:
        LOG.exception('Failed to query device')
        continue
      r[f'kasa_plug_{i+1}.power_w'] = e.power
      r[f'kasa_plug_{i+1}.consumption_kwh'] = e.total
      # TODO get daily usage?
      # r[f'kasa_plug_{i+1}.consumption_day_kwh'] = usage.usage_today
      # r[f'kasa_plug_{i+1}.consumption_month_kwh'] = usage.usage_this_month
    LOG.info(r)
    grafana.post('energy', interval=10, **r)


def parse_args():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)
  parser.add_argument('--discover', action='store_true')
  args = parser.parse_args()
  return args


if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    # level=logging.DEBUG,
    level=logging.INFO,
  )
  main(parse_args())
