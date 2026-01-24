
import argparse
import logging
import pprint
import sys


import tinytuya


LOG = logging.getLogger('tuya-test')


# TO DISCOVER THESE:
# python3 -m tinytuya wizard

GARAGE_METER = dict(
  dev_id='ebc712025315ecbf65tdgl',
  address='10.87.3.201',
  local_key='Z5s<);@i.R/4~g+z',
  version=3.4,
)

GARAGE_AIR = dict(
  dev_id='ebb9c933264b5e4c5fcskm',
  address='10.87.2.113',
  local_key="{fg]MK7?FD0$lyh3",
  version=3.5,
)

METER_KEYS = dict(
  relay_on = 1,


  potential_phaseA_dV = 101,
  current_phaseA_mA   = 102,
  power_phaseA_W      = 103,
  power_factor_phaseA = 104,
  energy_phaseA_daWh  = 105,

  potential_phaseB_dV = 107,
  current_phaseB_mA   = 108,
  power_phaseB_W      = 109,
  power_factor_phaseB = 110,
  energy_phaseB_daWh  = 111,

  potential_phaseC_dV = 113,
  current_phaseC_mA   = 114,
  power_phaseC_W      = 115,
  power_factor_phaseC = 116,
  energy_phaseC_daWh  = 117,

  energy_total_daWh   = 119,
  current_total_mA    = 120,
  power_total_W       = 121,
  frequency_Hz        = 122,



  # '123' = 0
  # '124' = 0
  # '125' = 26000
  # '126' = 26000
  # '127' = 26000
  # '128' = False
  # '129' = False
  # '130' = False

)
METER_KEYS = {str(v):k for k,v in METER_KEYS.items()}

AIR_KEYS = dict(
  air_quality_index = 1,
  temperature_C     = 2,
  humidity_percent  = 3,
  co2_ppm           = 4,
  ch2o_ugm3         = 5,
  pm0_3_ugm3        = 107,
  pm1_0_ugm3        = 8,
  pm2_5_ugm3        = 7,
  pm10_0_ugm3       = 9,
  formaldehyde_mgm3 = 6,
  battery_percent   = 22,
  battery_charging  = 23,
  tvoc_ugm3         = 101,
  temperature_units = 112,

)
AIR_KEYS = {str(v):k for k,v in AIR_KEYS.items()}


def fix_meter_keys(dps):
  return {METER_KEYS.get(k, f'n{k}'):v for k,v in dps.items()}

def fix_air_keys(dps):
  return {AIR_KEYS.get(k, f'n{k}'):v for k,v in dps.items()}

def grafana_filter(d):
  return {k:v for k,v in d.items() if isinstance(v, (int, float))}

def main(args):
  LOG.info(args)

  # d = tinytuya.Device(persist=True, **GARAGE_METER)
  d = tinytuya.Device(persist=True, **GARAGE_AIR)
  data = d.status()
  print(f'Device status: {data!r}')
  pd = fix_air_keys(data['dps'])
  print('DPS: \n%s' % pprint.pformat(pd))

  # grafana.post('garage_meter', interval=3600, **grafana_filter(pd))

  pd = {}
  while 1:
    data = d.receive()
    LOG.info(data)

    if data and (dps := data.get('dps')):
      pd.update(fix_air_keys(dps))
      LOG.info('\n' + pprint.pformat(pd))
      import grafana
      grafana.post('garage_air', interval=30, **grafana_filter(pd))
    else:
      d.heartbeat()



if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(funcName)s %(message)s',
    datefmt='%y%m%d-%H%M%S',
    # level=logging.DEBUG,
    level=logging.INFO,
  )

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)
  parser.add_argument('--ip', type=str, default='10.87.2.113')
  args = parser.parse_args()

  try:
    sys.exit(main(args))
  except KeyboardInterrupt:
    pass
