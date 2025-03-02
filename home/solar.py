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
  ss = utils.PySerial(ser, timeout=0.2)
  mppt = solar_mppt_ampinvt.MPPTAmpivnt(ss)
  ups = home2.KasaPlug('10.87.1.41', **KC)
  load = home2.KasaPlug('10.87.1.42', **KC)
  runner = homeutils.Runner()
  runner.add_async(ups)
  runner.add_async(load)

  last_battery_ok = time.time()
  last_load_shed = time.time()

  try:
    while 1:
      time.sleep(2)
      now = time.time()
      if now - last_battery_ok > 60:
        ups.turn_on()

      data = mppt.poll()
      LOG.info(data)
      if not data:
        LOG.info('no data')
        continue

      data = homeutils.DottedDict(data)

      grafana.post('solar', interval=10, **data)

      bv = data.battery_volts_cv * 1e-2

      cs = data.charging_status
      # TODO add bitflags to datum
      is_charging   = cs & (1<<0)
      is_equalizing = cs & (1<<1)
      is_mppt       = cs & (1<<2)
      is_float      = cs & (1<<3)
      # etc

      if bv > 57.48:
        # fully charged, about to enter float
        ups.turn_off()
        load.turn_on()


      def can_deep_cycle():
        # could we deep cycle and recover without the grid?
        base_load = 200 # TODO measure load2 avg
        # load_state = load.state('emeter')

        if bv < 46:
          LOG.warning('can\'t deep cycle: battery already too low!')

        # if not load_state:
        #   LOG.info('can\'t deep cycle: no load data')
        #   return False

        if data.charge_power_w < base_load:
          LOG.info('can\'t deep cycle: can\'t cover base load')
          return False

        # TODO would it even help?

        return True

      # Batteries are safe to go down to 46V, but the
      # UPS will try to charge the battery to 54.5V
      # We don't want to waste grid power to charge the batteries.
      if can_deep_cycle():
        # PSS will be 48 < bv < X
        if bv < 50:
          if (now - last_load_shed) > 60 * 4:
            # AC turn on cycle = 3 minutes.
            # (5-3)/5 = 40% min duty cycle
            # (5-4)/5 = 25% min duty cycle

            # TODO: do this with IR controls, not unplugging
            load.turn_off()
            # time.sleep(5.0)
            # load.turn_on()
            last_load_shed = now
        else:
          last_battery_ok = now

        continue # skips normal LV check


      if bv < 53.5:
        ups.turn_on()
        # TODO relax this if the net load on the battery is high
        # (indicating that it will jump back quickly)
        # net = 65 + load1 + load2 - mppt_power
      else:
        last_battery_ok = now

  except KeyboardInterrupt:
    LOG.info("Stop requested")
  finally:
    ups.turn_on()
    time.sleep(1)


def parse_args():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)
  parser.add_argument('--port', type=str, default='/dev/ttyUSB0')
  args = parser.parse_args()
  return args


if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(funcName)s %(message)s',
    datefmt='%y%m%d-%H%M%S',
    # level=logging.DEBUG,
    level=logging.INFO,
  )
  main(parse_args())
