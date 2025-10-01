import argparse
import inspect
import logging
import time
import pathlib



import dominate
import kasa
import requests
import whirl
from dominate import tags
from whirl.domx import dx


import utils
import grafana
import config
from devices import tuya


KC = config.CONF['kasa']
TD = config.CONF['tuya']['devices']

LOG = logging.getLogger(__name__)


# TODO move to devices/kasa
class Kasa(utils.Device):
  interval = 1.
  def check(self):
    if self.dev is None:
      raise utils.DeviceReset

  async def reset(self):
    LOG.info(f'Connecting to kasa device {self.a!r}')
    kd = kasa.Discover.discover_single(*self.a, **self.kw)
    LOG.info(f'{kd=}')
    dev = await kd
    self.dev = dev
    LOG.info(f'{dev=}')
    await dev.update()
    LOG.info(f'reset success')

  async def tick(self):
    self.check()
    LOG.debug(f"tick {self.dev=}")
    await self.dev.update()

    self.set_state('on', self.dev.is_on)

    if energy := self.dev.modules.get("Energy"):
      r = utils.DottedDict(
        power_w = energy.current_consumption,
        consumption_daily_kwh = energy.consumption_today,
        consumption_monthly_kwh = energy.consumption_this_month,
      )
      self.set_state('emeter', r)

    if devm := self.dev.modules.get("DeviceModule"):
      LOG.debug(f"{devm.data=!r}")
      if usage := devm.data.get('get_device_usage'):
        self.set_state('usage', usage)

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



class GrafanaUpdate(utils.Device):
  interval = 1.
  last_data = {}

  def tick(self):
    data = {}
    def add(dev, p):
      for k, (t, v) in dev.last_state.items():
        for p2, x in utils.dfs2(v):
          data['.'.join(p + (k,) + p2)] = (dev.interval, t, x)
    utils.dfs(DEVICES, add)
    last = self.last_data or {}
    self.last_data = data
    update = {k:v for k,v in data.items() if last.get(k) != v}
    post = []
    for k,v in update.items():
      try:
        fv = grafana.fix_value(v[2])
      except ValueError as e:
        LOG.warning(e)
        continue
      post.append(dict(
        name = k,
        value = fv,
        time = int(v[1]),
        interval = int(v[0] + 2),
      ))
    LOG.info(f'grafana: {post}')
    if post:
      grafana.post_frame(post)





class WebUI(utils.Device):
  interval = 0.
  def tick(self):
    whirl.domx.run(('', 8888))



DEVICES = utils.DottedDict(
  home = utils.DottedDict(
    light_office  = Kasa('10.87.1.51', **KC),
    light_shop    = Kasa('10.87.1.52', **KC),
    light_outside = Kasa('10.87.1.53', **KC),
    kitchen_kettle= Kasa('10.87.1.41', **KC),
    light_desk    = Kasa('10.87.1.42', **KC),
    attic_fan = tuya.Tuya(**TD['ATTIC_FAN']),
  ),
  power = utils.DottedDict(
    meter = tuya.Tuya(**TD['GARAGE_METER'])
  ),
  # rtl =
  # arduino =
  # pm =
  grafana = GrafanaUpdate(),
  webui = WebUI(),
)
DEVICES_FLAT = dict(utils.dfs2(DEVICES))


@whirl.domx.template
class HomePage(dominate.document):
  def __init__(self, title='Home', *a, **kw):
    super().__init__(title, *a, **kw)
    with self.head:
      tags.style(dominate.util.include('home.css'))

header = lambda x:tags.h2(tags.span(x))
class ctags:
  class power(tags.span): pass

@whirl.domx.route('/')
@tags.div
def index(url, handler):
  tags.h1('Hello world')
  tags.p(f'{url} {handler}')

  @tags.div(cls='device')
  def add(dev, path):
    path = '.'.join(path)
    tags.span(path)

    if hasattr(dev, 'turn_on'):
      match dev.state('on'):
        case None:
          c = ''
        case True:
          c = 'on'
        case False:
          c = 'off'
      with ctags.power(cls=c):
        tags.button('on',  dx(target='#content', get=f'/onoff/{path}/on'))
        tags.button('off', dx(target='#content', get=f'/onoff/{path}/off'))

    with tags.details():
      tags.summary()
      with tags.table():
        tags.tr(tags.th('key'), tags.th('value'))
        for k in dev.last_state.keys():
          tags.tr(tags.td(k), tags.td(repr(dev.state(k))))

  with tags.div(id='devices'):
    utils.dfs(DEVICES, add)

  with tags.div(id='content'):
    tags.p('log')


@whirl.domx.route(r'^/onoff/([^/]+)/(\w+)$')
@tags.div
def onoff(url, handler, path, state):
  path = tuple(path.split('.'))
  dev = DEVICES_FLAT[path]
  if state == 'on':
    dev.turn_on()
  if state == 'off':
    dev.turn_off()



def main(args):
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

  utils.dfs(DEVICES, add)

  try:
    while 1:
      print("hi")
      time.sleep(10)
  except KeyboardInterrupt:
    LOG.info("Stop requested")


if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    datefmt='%y%m%d-%H%M%S',
    # level=logging.DEBUG,
    level=logging.INFO,
  )

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  args = parser.parse_args()
  main(args)

