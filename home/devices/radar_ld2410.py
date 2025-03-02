
import argparse
import enum
import logging
import struct
import time

import serial

from devices import utils

LOG = logging.getLogger(__name__)


class RadarLD2410:

  class Command(enum.IntEnum):
    CONFIG_START                = 0x00FF,
    CONFIG_END                  = 0x00FE,
    SET_DISTANCE_AND_DURATION   = 0x0060,
    READ_PARAMETER              = 0x0061,
    ENGINEERING_START           = 0x0062,
    ENGINEERING_END             = 0x0063,
    SET_GATE_SENSITIVITY        = 0x0064,
    READ_FIRMWARE_VERSION       = 0x00A0,
    SET_BAUD_RATE               = 0x00A1,
    FACTORY_RESET               = 0x00A2,
    RESTART                     = 0x00A3,
    SET_BLUETOOTH               = 0x00A4,
    READ_MAC_ADDRESS            = 0x00A5,
    RESPONSE = 0x0100,


  # class Command(Datum):
  #   header: 'I' = 0xfafbfcfd
  #   length: 'H'
  #   cmd:    'H'
  #   data:   F(bytes, length='length') # plus 2 to account for cmd
  #   footer: 'I' = 0x01020304

  class FirmwareVersionFrame:
    fields = dict(
      command = 'H',
      ack     = 'H',
      type    = 'H',
      major1  = 'B',
      major2  = 'B',
      minor   = 'B',
    )
    STRUCT = struct.Struct('<' + ''.join(fields.values()))

  class TargetDataFrame:
    HEADER = 0xf1f2f3f4
    FOOTER = 0xf5f6f7f8
    fields = dict(
      header  = 'I',
      header2 = 'H',  # 0d00
      type    = 'B',  # 02
      head    = 'B',  # aa

      target_state              = 'B',
      motion_target_distance    = 'H',
      motion_target_energy      = 'B',
      static_target_distance    = 'H',
      static_target_energy      = 'B',
      detection_distance        = 'H',

      motion_max                = 'B',
      static_max                = 'B',
      # motion_energy = '8B',
      # static_energy = '8B',
      footer                    = 'I',
    )
    STRUCT = struct.Struct('<' + ''.join(fields.values()))

    @classmethod
    def unpack(cls, data):
      return dict(zip(
        cls.fields.keys(),
        cls.STRUCT.unpack(data)
      ))

  COMMAND_HEADER = 0xfafbfcfd
  COMMAND_FOOTER = 0x01020304

  def __init__(self, ser):
    self.ser = ser
    self.reset()

  def send_command(self, cmd, data=b''):
    params = [
      struct.pack('<I', self.COMMAND_HEADER), # header
      struct.pack('<H', len(data) + 2), # length
      struct.pack('<H', cmd),
      data, # stuff
      struct.pack('<I', self.COMMAND_FOOTER), # footer
    ]
    b = b''.join(params)
    self.ser.write(b)
    LOG.info(f'cmd:       {b.hex(" ", 2)}')
    response = self.ser.read_until(self.COMMAND_FOOTER.to_bytes(4, byteorder='little'), timeout=0.1)
    r = response
    if len(r) % 2 == 1:
      r += b'\x00'
    LOG.info(f'response: {r.hex(" ", 2)}')
    return response

  def reset(self):
    self.send_command(RadarLD2410.Command.FACTORY_RESET)
    self.send_command(RadarLD2410.Command.CONFIG_START, b'\x01\x00')

    # self.send_command(RadarLD2410.Command.READ_MAC_ADDRESS)
    self.send_command(RadarLD2410.Command.READ_FIRMWARE_VERSION)

    # self.send_command(RadarLD2410.Command.ENGINEERING_START)
    self.send_command(RadarLD2410.Command.CONFIG_END)




  def command(self, cmd):
    pass


  def poll(self):
    data = self.ser.read_until(self.TargetDataFrame.FOOTER.to_bytes(4, byteorder='little'))
    if not data:
      LOG.info('no data')
      self.reset()
      return

    # f3f2 f10d 0002 aa03 3c00 3600 0064 0000 5500 f8f7 f6f5


    # LOG.info(data.hex(' ', 2))
    assert len(data) == self.TargetDataFrame.STRUCT.size, (len(data), self.TargetDataFrame.STRUCT.size)

    frame = self.TargetDataFrame.unpack(data)

    assert frame.pop('header') == self.TargetDataFrame.HEADER
    assert frame.pop('footer') == self.TargetDataFrame.FOOTER
    assert frame.pop('header2') == 13
    assert frame.pop('type') == 2
    assert frame.pop('head') == 170


    assert frame.pop('static_max') == 0
    assert frame.pop('motion_max') == 85
    # assert frame.pop('detection_distance') == 0


    return frame




import toml
import requests
config = toml.load("config.toml")['grafana']

def post_grafana(ns, **kv):
  auth = 'Bearer {}:{}'.format(59684, config['grafana_token'])
  now = int(time.time())
  data = [{
    'name': '.'.join((ns, k)),
    'value': v,
    'time': now,
    'interval': 2,
  } for k,v in kv.items()]
  try:
    p = requests.post(
      config['grafana_uri'],
      headers={'Authorization': auth, 'Content-Type':'application/json'},
      json=data
    )
    LOG.info(p.json())
  except Exception as e:
    LOG.error(e)



def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  parser.add_argument('port', type=str, default='COM13')
  args = parser.parse_args()

  # cmd = RadarLD2410.Command()
  # print(cmd)

  ser = serial.Serial(
    args.port,
    baudrate=256000,
    parity='N',
    bytesize=8,
    stopbits=1,
    timeout=.1
  )
  ss = utils.PySerial(ser, timeout=0.1)

  ld2410 = RadarLD2410(ss)
  last = time.time()
  try:
    while 1:
      now = time.time()
      frame = ld2410.poll()
      print(frame)
      if now > last + 1:
        # post_grafana('radar_ld2410', **frame)
        last = now

  except KeyboardInterrupt:
    pass


# to run: (from parent dir)
# python -m devices.radar_ld2410 COM13

if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    level=logging.DEBUG,
    # level=logging.INFO,
  )
  main()
