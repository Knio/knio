import argparse
import logging
import time
import serial
import pathlib
import toml


import grafana
from devices import utils
from devices import kasa
from devices import solar_mppt_ampinvt

LOG = logging.getLogger('solar')

# TODO move this to util
config = toml.load(pathlib.Path(__file__).parent / 'config.toml')['kasa']


def main(args):
  ser = serial.Serial(
    args.port,
    baudrate=1200,
    parity='N',
    bytesize=8,
    stopbits=1,
    timeout=.1
  )
  ss = utils.PySerial(ser, timeout=0.1)
  mppt = solar_mppt_ampinvt.MPPTAmpivnt(ss)
  ups = kasa.Synced(kasa.discover('10.87.1.41', **config))
  ups.update()

  last_battery_ok = 0
  try:
    while 1:
      time.sleep(2)
      if time.time() - last_battery_ok > 60:
        ups.update()
        ups.turn_on()
      data = mppt.poll()
      LOG.info(data)
      if not data:
        continue
      grafana.post('solar', interval=10, **data)

      bv = data['battery_volts_cv'] * 1e-2
      if bv < 54.0:
        ups.update()
        ups.turn_on()
      elif bv > 56.9:
        ups.update()
        ups.turn_off()
      last_battery_ok = time.time()

  except KeyboardInterrupt:
    pass
  finally:
    ups.update()
    ups.turn_on()


def parse_args():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)
  parser.add_argument('--port', type=str, default='/dev/ttyUSB1')
  args = parser.parse_args()
  return args


if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    # level=logging.DEBUG,
    level=logging.INFO,
  )
  main(parse_args())
