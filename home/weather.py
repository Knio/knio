#! /usr/bin/python3
import json
import logging
import requests
import subprocess
import time
import toml


log = logging.getLogger('weather')

config = toml.load('config.toml')['grafana']

# https://grafana.com/docs/grafana-cloud/metrics-graphite/http-api/


def post_grafana(key, value):
  auth = 'Bearer {}:{}'.format(59684, config['grafana_token'])
  data = [{
    'name': 'rtl.' + key,
    'value': value,
    'time': int(time.time()),
    'interval': 60,
  }]
  try:
    p = requests.post(
      config['grafana_uri'],
      headers={'Authorization': auth, 'Content-Type':'application/json'},
      json=data
    )
    # log.info(p.text)
  except Exception as e:
    log.error(e)


def f_to_c(x):
  return (x - 32.) * 5. / 9.


def main():
  cmd = [
    'sudo',
    'rtl_433',
      '-F', 'json',
      '-C', 'si',
      # '-Y', 'autolevel',
      # '-Y', 'minmax',
      # '-Y', 'magest',
      '-M', 'level',
      '-M', 'noise',
  ]
  log.info(f"cmd: {' '.join(cmd)}")
  rtl = subprocess.Popen(cmd, stdout=subprocess.PIPE)

  def process(line):
    data = json.loads(line)
    line_s = line.decode('ascii').strip()
    if data.get('model') == 'Ambientweather-F007TH':
      id_ch_to_name_x = {
        (1, 222): ('House_Common', -0.200, -7.0),
        (2, 166): ('Outside_Back',  0.086, -3.0),
        (3, 51):  ('Inside_House',  0.146,  1.0),

        (1, 37):   ('Room',        -0.034, -1.0),
        (2, 14):   ('AC_Intake',   -0.114,  1.0),
        (3, 13):   ('AC_Cool',     -0.084,  0.0),

        (2,   3):  ('Freezer',        0.,  0.0),
        (1,  52):  ('Fridge',         0.,  0.0),
        (3, 114):  ('Tom_Cooler',     0.,  0.0),
      }
      ch_id = data.get('channel'), data.get('id')
      namex = id_ch_to_name_x.get(ch_id)
      if namex is None:
        log.warning(f'\n\nUnknown sensor: {line_s}\n\n')
      else:
        name, t_c, h_c = namex
        log.info(f'{name:<12s} {line_s}')
        post_grafana(f'Temperature_{name}', data['temperature_C'] - t_c)
        post_grafana(f'Humidity_{name}', data['humidity'] - h_c)
    else:
      log.warning(f'\n\nUnknown sensor: {line}\n\n')

  try:
    for line in rtl.stdout:
      process(line)
    if rtl.wait() != 0:
      print('''
  To proxy usb to WSL2:
  usbipd wsl attach  -b 11-4 -d Ubuntu-20.04
  ''')

  except KeyboardInterrupt:
    # rtl.send_signal(2)
    return



if __name__ == '__main__':
  logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)s: %(message)s')

  logging.getLogger('urllib3').setLevel(logging.WARNING)

  main()
