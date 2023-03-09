'''

'''

import argparse
import json
import logging
import requests
import threading
import time

import serial
import dl24

log = logging.getLogger('lab')

GRAFANA_USER = 'air-sensor'
GRAFANA_TOKEN = 'eyJrIjoiMDE2ZWQ1MjNhMDJjZDNjZWFjZjEzNjY5ZGExYTBlMmU4M2FlZDQwYiIsIm4iOiJhaXItc2Vuc29yIiwiaWQiOjQ3MjU3Mn0='
GRAFANA_URI = 'https://graphite-us-central1.grafana.net/metrics'
# https://hjklca.grafana.net
# https://grafana.com/docs/grafana-cloud/metrics-graphite/http-api/


def post_grafana(key, value):
  auth = 'Bearer {}:{}'.format(59684, GRAFANA_TOKEN)
  data = [{
    'name': 'lab.' + key,
    'value': value,
    'time': int(time.time()),
    'interval': 60,
  }]
  try:
    p = requests.post(
      GRAFANA_URI,
      headers={'Authorization': auth, 'Content-Type':'application/json'},
      json=data
    )
    # log.info(p.text)
  except Exception as e:
    log.error(e)


def dl24m(ser):
  dev = dl24.DL24M(ser)
  while 1:
    try:
      p = dev.get_state()
      print(f'state: {p!r}')

      mv = dev.get_millivolts()
      print(f'V: {mv} mV')

      ma = dev.get_milliamps()
      print(f'I: {ma} mA')

      et = dev.get_time()
      print(f'T: {et}')

      mah = dev.get_milliamphours()
      print(f'C: {mah} mAh')

      mwh = dev.get_milliwatthours()
      print(f'T: {mwh} mWh')

      deg = dev.get_temp2()
      print(f'E: {deg} C')

      val = dev.get_limit_value()
      print(f'L?: {val} ?')

      lv = dev.get_min_voltage()
      print(f'LV: {lv:.2f} V')

      lt = dev.get_max_time()
      print(f'LT: {lt}')

      md = dev.get_mode()
      print(f'M: {md!r}')

      xx01 = dev.get_xx01()
      print(f'XX01: {xx01!r}')

      xx = b''
      # for i in range(0x22, 0x40):
      #   x = dev.get_value(i)
      #   xx += x
      #   print(f'XX {i:02x}: {x.hex(" ", 4)}')
      # print(f'XX: {xx.hex()}')

    except:
      log.exception('error while querying')

    ser.timeout = .1
    b = ser.read(128)
    if b:
        print(f'extra bytes: {b.hex(" ", 4)}')



'''

ff 550102 0000c2 000794 000002 000000 000000 000000 000000 150000 00003c 000000 00c500
               ^      ^      ^                              ^                   ^
       voltage |      |      |                              |
              current |      |                              | temp
                     minutes |



'''

def main():
  print('hello world')

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('port', type=str, default='COM9')
  args = parser.parse_args()

  ser = serial.Serial(
    args.port,
    # baudrate=9600,
    # bytesize=8,
    # stopbits=1,
    timeout=2.
  )

  dl24m_thread = threading.Thread(target=dl24m, args=(ser,))
  dl24m_thread.daemon = True
  # dl24m_thread.start()

  dev = dl24.DL24M(ser)
  try:
    pass
    # dev.set_mode(dl24.DL24M.Mode.CURRENT)
  except:
    pass
  # time.sleep(.2)
  # dev.set_cmd(dl24.DL24M.Command.BATTERY_SIZE, dl24.DL24M.BatterySize.SMALL)
  # c = dev.get_clear()
  # print(f'clear: {c:x}')
  dev.set_min_voltage(2)
  dev.set_max_time()
  # dev.set_power_on()
  dev.set_power_off()
  dev.set_mode(dl24.DL24M.Mode.CURRENT)
  dev.set_limit(3)
  # dev.set_power_on()
  # dev.reset_counters()
  return
  # dev.set_mode(dl24.DL24M.Mode.BATTERY)
  # dev.set_cmd(0x08, 0x01)
  # dev.set_mode(dl24.DL24M.Mode.POWER_SUPPLY)

  # time.sleep(.5)
  # dev.set_cmd(dl24.DL24M.Command.BATTERY_SIZE, c=dl24.DL24M.BatterySize.SMALL)
  # time.sleep(.5)
  # dev.set_cmd(dl24.DL24M.Command.BATTERY_SIZE, c=dl24.DL24M.BatterySize.BIG)
  # dev.set_power_on()
  # time.sleep(1)
  # return
  try:
    while 1:
      ser.timeout = 1
      b = ser.read_all()
      if b:
        print('\n' + b.hex(' ', 2))
      else:
        print('.', end='', flush=True)
        time.sleep(.2)
  except KeyboardInterrupt:
    return

  dev.set_power_off()
  dev.reset_counters()
  return

  for i in range(16):
    print(i)
    try:
      pass
      # dev.set_mode(i)
    except:
      log.exception('')
    time.sleep(5)
  # dev.set_limit(10)
  # dev.set_min_voltage(2.7)


if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
  )
  logging.getLogger('urllib3').setLevel(logging.WARNING)
  main()

