#! /usr/bin/python3
import json
import logging
import requests
import subprocess
import time
import toml

import grafana

LOG = logging.getLogger('weather')


def f_to_c(x):
  return (x - 32.) * 5. / 9.


def main():
  cmd = [
    'sudo',
    'rtl_433',
      '-F', 'json',
      '-C', 'si',
      '-f', '433.926M',
      # '-Y', 'autolevel',
      # '-Y', 'minmax',
      # '-Y', 'magest',
      '-M', 'level',
      '-M', 'noise',
  ]
  LOG.info(f"cmd: {' '.join(cmd)}")
  rtl = subprocess.Popen(cmd, stdout=subprocess.PIPE)

  def process(line):
    data = json.loads(line)
    line_s = line.decode('ascii').strip()
    if data.get('model') == 'Ambientweather-F007TH':
      id_ch_to_name_x = {
        (1, 201): ('House_Common', -0.200, -7.0),
        (2, 166): ('Outside_Back',  0.086, -3.0),
        (3, 38):  ('Bathroom',  0.146,  1.0),

        (1, 97):   ('Room',        -0.034, -1.0),
        (2, 14):   ('AC_Intake',   -0.114,  1.0),
        (3, 13):   ('AC_Cool',     -0.084,  0.0),

        (2,   3):  ('Freezer',        0.,  0.0),
        (1,  14):  ('Fridge',         0.,  0.0),
        (3, 114):  ('Tom_Cooler',     0.,  0.0),
      }
      ch_id = data.get('channel'), data.get('id')
      namex = id_ch_to_name_x.get(ch_id)
      if namex is None:
        LOG.warning(f'\n\nUnknown sensor: {line_s}\n\n')
      else:
        name, t_c, h_c = namex
        LOG.info(f'{name:<12s} {line_s}')
        grafana.post('rtl',
          interval=300,
          **{
            f'Temperature_{name}': data['temperature_C'] - t_c,
            f'Humidity_{name}': data['humidity'] - h_c,
          }
        )
    else:
      LOG.warning(f'\n\nUnknown sensor: {line}\n\n')

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
    datefmt='%y%m%d-%H%M%S',
    format='%(asctime)s:%(levelname)s:%(filename)s:%(lineno)s:%(funcName)s: %(message)s')

  logging.getLogger('urllib3').setLevel(logging.WARNING)

  main()
