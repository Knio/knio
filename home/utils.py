
import logging
import asyncio
import time
import threading


LOG = logging.getLogger(__name__)


class Device:
  interval = 1.
  def __init__(self, *a, **kw):
    self.a = a
    self.kw = kw
    self.dev = None
    self.last_state = {}

  def set_state(self, name=None, x=None, timeout=0.):
    LOG.debug(f'set_state({name!r}, {x!r})')
    self.last_state[name] = time.time(), x

  def state(self, name=None, timeout=None):
    if timeout is None:
      timeout = self.interval
    t, x = self.last_state.get(name, (0, None))
    if t + timeout < time.time():
      return None
    return x

  def reset(self):
    pass


class Runner:
  def __init__(self):
    self.threads = []
    self.tasks = []

    self.loop = asyncio.new_event_loop()
    self.loop_thread = threading.Thread(target=self.loop.run_forever)
    self.loop_thread.daemon = True
    self.loop_thread.start()
    self.threads.append(self.loop_thread)

  # todo context manager
  def __del__(self):
    self.loop.stop()

  def add_thread(self, dev):
    def thread_loop():
      LOG.info("thread_loop")
      while 1:
        try:
          dev.runner = self
          r = dev.tick()
        except:
          LOG.exception('')
          try:
            dev.reset()
          except:
            LOG.exception('')
          time.sleep(10)
        time.sleep(dev.interval)

    t = threading.Thread(target=thread_loop)
    t.daemon = True
    t.start()
    self.threads.append(t)

  def add_async(self, dev):
    async def aio_loop():
      LOG.info("aio_loop")
      while 1:
        try:
          dev.runner = self
          r = await dev.tick()
        except:
          LOG.exception('')
          await asyncio.sleep(10)
          try:
            await dev.reset()
          except:
            LOG.exception('')
        await asyncio.sleep(dev.interval)

    f = self.start_async(aio_loop())
    self.tasks.append(f)

  def start_async(self, coro):
    return asyncio.run_coroutine_threadsafe(coro, self.loop)
