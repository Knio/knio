import logging
import argparse
import dataclasses
import inspect
import functools
import time
import asyncio

import kasa

import utils
import grafana
import config


KC = config.CONF['kasa']

LOG = logging.getLogger(__name__)


class KasaPlug(utils.Device):
  interval = 1.
  def check(self):
    if self.dev is None:
      raise utils.DeviceReset

  async def reset(self):
    LOG.info(f'Connecting to kasa device {self.a!r}')
    kd = kasa.Discover.discover_single(*self.a, **self.kw)
    dev = await kd
    await dev.update()
    self.dev = dev

  async def tick(self):
    LOG.debug("tick")
    self.check()
    await self.dev.update()
    energy = self.dev.modules["Energy"]
    # await energy.get_status() # TODO doesn't update!!
    # do this instead and take raw values:
    # have to do own error checking
    # res = await energy.call("get_energy_usage")
    r = utils.DottedDict(
      power_w = energy.current_consumption,
      consumption_daily_kwh = energy.consumption_today,
      consumption_monthly_kwh = energy.consumption_this_month,
    )
    self.set_state('emeter', r)

  def turn_on(self):
    if self.dev is None:
      LOG.warning(f"Attempt to turn on {self!r} but it's not initialized")
      return
    LOG.info(f'Turning on plug {self.a!r}')
    return self.runner.start_async(self.dev.turn_on())

  def turn_off(self):
    if self.dev is None:
      LOG.warning(f"Attempt to turn off {self!r} but it's not initialized")
      return
    LOG.info(f'Turning off plug {self.a!r}')
    return self.runner.start_async(self.dev.turn_off())


class KasaSwitch(KasaPlug):
  interval = 60.
  async def tick(self):
    self.check()
    await self.dev.update()


def dfs(root, f, path=()):
  for k, v in root.items():
    p = path + (k,)
    if isinstance(v, dict):
      dfs(v, f, p)
    else:
      f(v, p)


def dfs2(root, path=()):
  for k, v in root.items():
    p = path + (k,)
    if isinstance(v, dict):
      yield from dfs2(v, p)
    else:
      yield p, v


class GrafanaUpdate(utils.Device):
  interval = 1.
  last_data = {}

  def tick(self):
    data = {}
    def add(dev, p):
      for k, (t, v) in dev.last_state.items():
        for p2, x in dfs2(v):
          data['.'.join(p + (k,) + p2)] = (dev.interval, t, x)
    dfs(DEVICES, add)
    last = self.last_data or {}
    self.last_data = data
    update = {k:v for k,v in data.items() if last.get(k) != v}
    post = [dict(
      name = k,
      value = v[2],
      time = int(v[1]),
      interval = int(v[0] + 2),
    ) for k,v in update.items()]
    LOG.debug(post)
    if post:
      grafana.post_frame(post)



DEVICES = utils.DottedDict(
  kasa = utils.DottedDict(
    plug_1 = KasaPlug('10.87.1.41', **KC),
    plug_2 = KasaPlug('10.87.1.42', **KC),
    plug_3 = KasaPlug('10.87.1.43', **KC),
    plug_4 = KasaPlug('10.87.1.44', **KC),

    light_1 = KasaSwitch('10.87.1.25'),
    light_2 = KasaSwitch('10.87.1.26'),
  ),
  # rtl =
  # arduino =
  # pm =
  grafana = GrafanaUpdate()
)


def home(args):

  runner = utils.Runner()

  def add(dev, p):
    LOG.info(f'add{dev!r}')
    t = dev.tick
    if inspect.iscoroutinefunction(t):
      LOG.info(f'add_async {dev!r}')
      runner.add_async(dev)
    else:
      LOG.info(f'add_thread {dev!r}')
      runner.add_thread(dev)

  dfs(DEVICES, add)

  try:
    while 1:
      print("hi")
      time.sleep(10)
  except KeyboardInterrupt:
    LOG.info("Stop requested")


def main():
  logging.basicConfig(
    # level=logging.DEBUG,
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s')

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  args = parser.parse_args()

  home(args)


if __name__ == '__main__':
  main()

