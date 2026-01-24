import logging

import tinytuya

import utils


LOG = logging.getLogger(__name__)


class Tuya(utils.Device):
  interval = 5.
  timeout = 30.
  def reset(self):
    self.dev = tinytuya.Device(persist=True, **self.kw)

  def tick(self):
    if not self.dev:
      raise utils.DeviceReset
    pd = {}
    self.dev.heartbeat()
    data = self.dev.receive()
    if data:
      # TODO map keys
      pd.update(data)
      LOG.info(f'{pd=}')
      self.set_state('data', pd)
    status = self.dev.status()
    LOG.info(f'{status=}')
    self.set_state('status', status)
    if (s := status.get('dps', {}).get('1')) is not None:
      self.set_state('on', s)

  def turn_on(self):
    self.dev.turn_on()

  def turn_off(self):
    self.dev.turn_off()



