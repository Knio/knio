import asyncio
import logging

import kasa

import config


# TODO:
'''
Don't use this module? replace with whats in utils and home2.py
'''

LOG = logging.getLogger(__name__)
AIOL = asyncio.get_event_loop()
KC = config.CONF['kasa']


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
    self.dev.turn_on()
    AIOL.run_until_complete(self.dev.update())

  def turn_off(self):
    AIOL.run_until_complete(self.dev.turn_off())

  def emeter(self):
    return AIOL.run_until_complete(self.dev.get_emeter_realtime())

SmartDimmer = lambda *x,**kw: Synced(kasa.SmartDimmer(*x, **KC, **kw))
