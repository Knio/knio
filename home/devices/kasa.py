import asyncio
import logging

import kasa

LOG = logging.getLogger(__name__)
AIOL = asyncio.get_event_loop()

class SmartPlug(kasa.SmartPlug):
  def __init__(self, *a, **kw):
    super().__init__(*a, **kw)
    self.update()

  def update(self):
    AIOL.run_until_complete(super().update())

  def turn_on(self):
    AIOL.run_until_complete(super().turn_on())

  def turn_off(self):
    AIOL.run_until_complete(super().turn_off())

  def emeter(self):
    return AIOL.run_until_complete(super().get_emeter_realtime())

def discover(*a, **kw):
  return AIOL.run_until_complete(kasa.Discover.discover_single(*a, **kw))


class Synced:
  def __init__(self, dev):
    self.dev = dev

  def update(self):
    AIOL.run_until_complete(self.dev.update())

  def turn_on(self):
    AIOL.run_until_complete(self.dev.turn_on())

  def turn_off(self):
    AIOL.run_until_complete(self.dev.turn_off())

  def emeter(self):
    return AIOL.run_until_complete(self.dev.get_emeter_realtime())

