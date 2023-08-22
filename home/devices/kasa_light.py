import asyncio
import logging

import kasa

LOG = logging.getLogger(__name__)


class Light(kasa.SmartPlug):
  aiol = asyncio.get_event_loop()
  def __init__(self, *a, **kw):
    super().__init__(*a, **kw)
    self.update()

  def update(self):
    self.aiol.run_until_complete(super().update())

  def turn_on(self):
    self.aiol.run_until_complete(super().turn_on())

  def turn_off(self):
    self.aiol.run_until_complete(super().turn_off())


