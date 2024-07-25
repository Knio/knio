# coding=utf8

import logging
import time

import msvcrt
import pynput.keyboard
import pynput.mouse


log = logging.getLogger('pj')


def get_key():
  if msvcrt.kbhit():
    k = msvcrt.getch()
    if k == b'\xe0':
      k += msvcrt.getch()
    return k.hex()


class Translator(object):
  def __init__(self, kb, mouse):
    self.kb = kb
    self.mouse = mouse
    self.remap_scroll = False
    self.capture_pt = None
    self.scroll_pt = 0,0

    self.kb_listener = pynput.keyboard.Listener(
        # on_press=self.handle_kb_press,
        # on_release=self.handle_kb_release,
    # )
        win32_event_filter=self.handle_kb_filter)

    self.mouse_listener = pynput.mouse.Listener(
        # on_move=self.handle_mouse_move,
        # on_click=self.handle_mouse_click,
        # on_scroll=self.handle_mouse_scroll,
        win32_event_filter=self.handle_mouse_filter)

  def handle_mouse_move(self, *x):
    log.debug(f'mouse_move {x}')

  def handle_mouse_click(self, *x):
    log.debug(f'mouse_click {x}')
    pass

  def handle_mouse_scroll(self, *x):
    pass

  def handle_mouse_filter(self, msg, llhook):
    # https://learn.microsoft.com/en-gb/windows/win32/api/winuser/ns-winuser-msllhookstruct
    pt = llhook.pt.x, llhook.pt.y
    data = llhook.mouseData
    flags = llhook.flags
    time = llhook.time

    log.debug(f'mouse_filter msg:{msg}, pt:{pt}, data:{data}, flags:{flags}, time:{time}')

    if not self.capture_pt:
      self.capture_pt = pt

    WM_XBUTTONDOWN = 523
    WM_XBUTTONUP = 524

    if msg == 512 and self.remap_scroll == 2:
      dx = pt[0] - self.capture_pt[0]
      dy = pt[1] - self.capture_pt[1]
      self.scroll_pt = (
        self.scroll_pt[0] + dx,
        self.scroll_pt[1] + dy
      )
      # log.info(f'capture mouse: {dx},{dy}')
      log.info(f'capture mouse: {self.capture_pt} {self.mouse.position} {pt} ({dx},{dy}) {self.scroll_pt}')

      self.mouse_listener.suppress_event()
      return False

    self.capture_pt = pt

  def handle_kb_press(self, x):
    log.debug(f'kb_press {x!r}')

  def handle_kb_release(self, x):
    log.debug(f'kb_release {x!r}')

  def handle_cli(self, x):
    if x is None: return

    log.debug(f'cli {x!r}')
    if x == '63':
      raise KeyboardInterrupt
    if x == '1b':
      raise KeyboardInterrupt

  def handle_kb_filter(self, id, data):
    # https://learn.microsoft.com/en-gb/windows/win32/api/winuser/ns-winuser-kbdllhookstruct
    log.debug(f'kb_filter id:{id}, vk:{data.vkCode}, scan:{data.scanCode}, flags:{data.flags}')

    if self.remap_scroll == 0 and data.vkCode == 91 and data.flags == 1:
      log.info('remap_scroll 1')
      self.remap_scroll = 1
      # TODO suppress winkey and replay if it was not a D
      self.kb_listener.suppress_event()
      return False

    if self.remap_scroll == 1 and data.vkCode == 68 and data.flags == 0:
      log.info('remap_scroll 2')
      self.remap_scroll = 2
      self.scroll_pt = 0,0
      log.info(f'pt: {self.capture_pt!r}')
      self.kb_listener.suppress_event()
      return False

    if self.remap_scroll == 2 and data.vkCode == 91 and data.flags == 1:
      log.debug('remap_scroll repeat 1')
      self.kb_listener.suppress_event()
      return False

    if self.remap_scroll == 2 and data.vkCode == 68 and data.flags == 0:
      log.debug('remap_scroll repeat 2')
      self.kb_listener.suppress_event()
      return False

    if self.remap_scroll == 2 and data.vkCode == 91 and data.flags == 129:
      log.info('remap_scroll 3')
      self.remap_scroll = 3
      self.kb_listener.suppress_event()
      return False

    if self.remap_scroll == 3 and data.vkCode == 68 and data.flags == 128:
      log.info('remap_scroll 0')
      self.remap_scroll = 0
      self.capture_pt = None

    # TODO: reply winkey if it wasn't our custom command
    # TODO: middle click

    self.remap_scroll = 0
    return True

  def kb_press(self, k):
    self.kb.press(k)
    self.kb.release(k)

  def run(self):
    # pynput monitors run on their own threads
    self.kb_listener.start()
    self.kb_listener.wait()
    self.mouse_listener.start()
    self.mouse_listener.wait()

    # mainloop poll mcu and cli
    try:
      while 1:
        if self.remap_scroll == 2:
          scale = 50
          dx = self.scroll_pt[0] // scale
          dy = self.scroll_pt[1] // scale
          if abs(dx) >= 1 or abs(dy) >= 1:
            log.info(f'scroll {dx},{dy}')
            self.mouse.scroll(-dx, dy)
            self.scroll_pt = (
              self.scroll_pt[0] - dx * scale,
              self.scroll_pt[1] - dy * scale
            )
          time.sleep(0.01)
        else:
          time.sleep(0.05)
        self.handle_cli(get_key())

    finally:
      self.kb_listener.stop()
      self.mouse_listener.stop()
      self.kb.release(Key.cmd)


Key = pynput.keyboard.Key
Key.stop = pynput.keyboard.KeyCode(vk=178)


def main():
  k = pynput.keyboard.Controller()
  m = pynput.mouse.Controller()
  t = Translator(k, m)
  try:
    t.run()
  except KeyboardInterrupt:
    pass


if __name__ == '__main__':
  logging.basicConfig(
    # level=logging.DEBUG,
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)s: %(message)s')

  logging.getLogger('urllib3').setLevel(logging.WARNING)

  main()

