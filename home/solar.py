import argparse
import logging
import time
import serial

from devices import utils
from devices import kasa
from devices import solar_mppt_ampinvt

import grafana
import config

# TODO
import home2
import utils as homeutils

LOG = logging.getLogger('solar')

KC = config.CONF['kasa']



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
  ups = home2.KasaPlug('10.87.1.41', **KC)
  runner = homeutils.Runner()
  runner.add_async(ups)

  last_battery_ok = 0
  try:
    while 1:
      time.sleep(2)
      if time.time() - last_battery_ok > 60:
        ups.turn_on()
      data = mppt.poll()
      LOG.info(data)
      if not data:
        continue
      grafana.post('solar', interval=10, **data)

      bv = data['battery_volts_cv'] * 1e-2
      # Batteries are safe to go down to 46V, but the
      # UPS will try to charge the battery to 54.5V
      # We don't want to waste grid power to charge the batteries.
      if bv < 53.5:
        ups.turn_on()
      elif bv > 56.9:
        ups.turn_off()
      last_battery_ok = time.time()

  except KeyboardInterrupt:
    LOG.info("Stop requested")
  finally:
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
    level=logging.DEBUG,
    # level=logging.INFO,
  )
  main(parse_args())
