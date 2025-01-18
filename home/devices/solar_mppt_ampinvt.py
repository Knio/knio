'''

'''

import time
import argparse
import logging
import serial
import enum

from devices import utils
from devices import datum



class Protocol:
  class Command(enum.IntEnum):
    QUERY_STATUS    = 0xa1
    QUERY_SETTINGS  = 0xa2
    QUERY_REALTIME  = 0xa3
    COMMAND_STATE   = 0xc0



# pyright: reportInvalidTypeForm=false
class MPPTCommand(datum.Datum):
  address:  datum.u8
  command:  datum.u8(enum=Protocol.Command)
  control:  datum.u8 = 0
  data:     datum.u32 = 0
  checksum: datum.u8 = 0

class MPPTRealtimeStatus(datum.Datum):
  address:              datum.u8
  command:              datum.u8
  control:              datum.u8
  operating_status:     datum.u8
  charging_status:      datum.u8
  control_status:       datum.u8
  pv_volts_dv:          datum.u16
  battery_volts_cv:     datum.u16
  charge_current_ca:    datum.u16
  internal1_temperature_dc:  datum.u16
  internal2_temperature_dc:  datum.u16
  external_temperature_dc:   datum.u16
  reserved0:            datum.u16
  # daily_power_hw:       datum.u32
  # total_power_hw:       datum.u32
  # reserved1:            datum.u32
  # reserved2:            datum.u32
  checksum:             datum.u8



LOG = logging.getLogger(__name__)


class MPPTAmpivnt:
  def __init__(self, ss):
    self.serial = ss
    self.serial.timeout = 1


  def poll(self):
    # TODO need a .read_n()
    # d = self.serial.read_all()

    cmd = MPPTCommand(
      address=101,
      command=Protocol.Command.QUERY_REALTIME,
      control=1,
    )
    cmd.checksum = sum(cmd.serialize()[:6]) & 0xff

    LOG.debug(f'cmd: {cmd!r}')
    cmd_bytes = cmd.serialize()
    LOG.debug(f'bytes: ({len(cmd_bytes)}) {cmd_bytes.hex(" ")}')

    response = MPPTRealtimeStatus()
    self.serial.write(cmd_bytes)
    d = self.serial.read_all()
    LOG.debug(f'{len(d)} {d.hex(" ")}')
    if len(d) < response.size():
      LOG.info(f'Ignoring incomplete data: ({len(d)} != {response.size()}): {d.hex()}')
      return
    d = d[:response.size()]

    response.deserialize_into(d)

    data = response.dict()
    del data['checksum']
    del data['reserved0']
    del data['internal2_temperature_dc']
    data['charge_power_w'] = response.battery_volts_cv * response.charge_current_ca * 1e-4
    return data

def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('port', type=str, default='/dev/ttyUSB1')
  args = parser.parse_args()

  ser = serial.Serial(
    args.port,
    baudrate=1200,
    parity='N',
    bytesize=8,
    stopbits=1,
    timeout=.1
  )
  ss = utils.PySerial(ser, timeout=0.1)
  mppt = MPPTAmpivnt(ss)

  try:
    while 1:
      print(mppt.poll())
      time.sleep(2)

  except KeyboardInterrupt:
    pass


# to run: (from parent dir)
# python -m devices.solar_mppt_ampinvt COM18

if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    datefmt='%y%m%d-%H%M%S',
    level=logging.DEBUG,
    # level=logging.INFO,
  )
  main()
