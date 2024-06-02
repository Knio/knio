# coding=utf8

import json
import logging
import subprocess
import threading
import time
import toml

import msvcrt
import pynput.keyboard
import pynput.mouse
import serial
import requests


log = logging.getLogger('cir')


S = 'S'
N = 'N'

class Sony(object):
  A = (S, 0x30)
  POWER     = 'S.30.15'
  VOL_UP    = 'S.30.12'
  VOL_DOWN  = 'S.30.13'
  INPUT_TV  = 'S.30.6A'
  INPUT_BD  = 'S.10.16.28'

class Denon(object):
  POWER     = 'D.9805.0280'
  VOL_UP    = 'D.9805.003A'
  VOL_DOWN  = 'D.9805.023A'
  ENTER     = 'D.9805.03E0'
  UP        = 'D.9805.0360'
  DOWN      = 'D.9805.00E0'
  LEFT      = 'D.9805.02E0'
  RIGHT     = 'D.9805.01E0'
  PLAY_PAUSE= 'D.9805.001F'
  PREV      = 'D.9805.031F'
  NEXT      = 'D.9805.091F'

class Light(object):
  ON =      'N.00.45'
  OFF =     'N.00.47'
  WHITE =   'N.00.46'
  LO =      'N.00.40'
  BRIGHTER= 'N.00.15'
  DIMMER =  'N.00.09'
  USER1 =   'N.00.16'
  USER2 =   'N.00.19'
  USER3 =   'N.00.0D'

class Projector(object):
  ON =            'N.F483.87'
  OFF =           'N.F483.A1'
  INPUT_HDMI1 =   'N.F483.A7'
  INPUT_HDMI2 =   'N.F483.A8'

class Fan(object):
  MODE        = 'B.02.39'
  TEMP_UP     = 'B.02.3C'
  TEMP_DOWN   = 'B.02.5F'
  TEMP_MODE   = 'B.02.6F'
  DIRECTION   = 'B.02.77'

class AC(object):
  POWER       = 'N.6681.81'
  TEMP_DOWN   = 'N.6681.8A'
  TEMP_UP     = 'N.6681.85'
  FAN         = 'N.6681.99'
  MODE        = 'N.6681.9B'
  TIMER       = 'N.6681.9F'


config = toml.load("config.toml")['grafana']


def post_grafana(kv):
  auth = 'Bearer {}:{}'.format(59684, config['grafana_token'])
  data = [{
    'name': 'cir.' + k,
    'value': v,
    'time': int(time.time()),
    'interval': 13,
  } for k,v in kv.items()]
  try:
    p = requests.post(
      config['grafana_uri'],
      headers={'Authorization': auth, 'Content-Type':'application/json'},
      json=data
    )
    # log.info(p)
    log.info(p.text)
  except Exception as e:
    log.error(e)


class CIR(object):
  def __init__(self, ser):
    self.ser = ser
    self.buffer = ''
    self.last = (0, None)

  def send(self, s):
    log.info(s)
    self.ser.write(s.encode('ascii') + b'\r')
    self.ser.flush()

  def poll(self):
    while 1:
      line = self.ser.readline().decode('ascii', 'replace')
      if not line: break
      # log.debug(repr(line))
      self.buffer += line
    self.buffer, *rest = self.buffer.split('\n', 1)
    if not rest:
      return
    cmd = self.buffer.strip()
    self.buffer = rest[0]
    now = time.time()
    if (now - self.last[0]) < 0.15 and (cmd == self.last[1] or cmd == 'E.00.00'):
      return
    # log.info((now - self.last[0]))
    self.last = now, cmd
    log.info(cmd)
    return cmd


class Keybow(object):
  def __init__(self, ser):
    self.ser = ser
    self.buffer = []
    self.thread = threading.Thread(target=self.run, daemon=True)
    self.thread.start()

  def run(self):
    while 1:
      line = self.ser.readline().decode('ascii', 'replace')
      if not line: continue
      cmd = line.strip()
      log.info('Keybow: %s', cmd)
      if cmd.startswith('CMD'):
        self.buffer.append(cmd.split(' ', 1)[1])
    log.info('Keybow thread done')

  def poll(self):
    if self.buffer:
      return self.buffer.pop(0)


def get_key():
  if msvcrt.kbhit():
    k = msvcrt.getch()
    if k == b'\xe0':
      k += msvcrt.getch()
    return k.hex()


keys = {
  b'\xe0H': Sony.VOL_UP,
  b'\xe0P': Sony.VOL_DOWN,

  b'\r': Light.ON,
  b'.': Light.OFF,
  b'+': Light.WHITE,
  b'-': Light.LO,

  b'\xe0I': Fan.MODE,      # pgup
  b'\xe0Q': Fan.DIRECTION, # pgdn

}


class Translator(object):
  mapping = {}

  def __init__(self, cir, kb, mouse, keybow):
    self.cir = cir
    self.kb = kb
    self.mouse = mouse
    self.keybow = keybow

    self.kb_listener = pynput.keyboard.Listener(
        on_press=self.handle_kb_press,
        on_release=self.handle_kb_release,
        win32_event_filter=self.handle_kb_filter)

    self.mouse_listener = pynput.mouse.Listener(
        on_move=self.handle_mouse_move,
        on_click=self.handle_mouse_click,
        on_scroll=self.handle_mouse_scroll,
        win32_event_filter=self.handle_mouse_filter)

  def handle_mouse_move(self, *x):
    pass

  def handle_mouse_click(self, *x):
    log.info(f'click {x}')
    pass

  def handle_mouse_scroll(self, *x):
    pass

  def handle_mouse_filter(self, *x):
    # log.info(f'filter {x}')
    msg, hook = x
    # log.info(f'hook {hook.mouseData}')

    # TODO dispatch these with handle function and move to
    # KnioTranslator

    WM_XBUTTONDOWN = 523
    WM_XBUTTONUP = 524

    button = hook.mouseData >> 16
    if button == 1:
      if msg == WM_XBUTTONDOWN:
        self.kb.press(Key.enter)
        self.mouse_listener.suppress_event()
        return False
      elif msg == WM_XBUTTONUP:
        self.kb.release(Key.enter)
        self.mouse_listener.suppress_event()
        return False
    if button == 2:
      if msg == WM_XBUTTONDOWN:
        self.kb.press(Key.esc)
        self.mouse_listener.suppress_event()
        return False
      elif msg == WM_XBUTTONUP:
        self.kb.release(Key.esc)
        self.mouse_listener.suppress_event()
        return False

    return

    x, y, button, pressed = x
    # TODO dispatch these with handle function and move to
    # KnioTranslator
    try:
      if button == pynput.mouse.Button.x1:
        if pressed:
          self.kb.press(Key.enter)
        else:
          self.kb.release(Key.enter)
    except:
      import traceback
      log.error(traceback.format_exc())

    pass

  def handle_kb_press(self, x):
    pass

  def handle_kb_release(self, x):
    pass

  def handle_kb_filter(self, msg, data):
    # log.info('%r %r', msg, data)
    # log.info('%r', dir(data))
    log.info('vk: %s, scan: %s, flags: %s', data.vkCode, data.scanCode, data.flags)

    # TODO dispatch these with handle function and move to
    # KnioTranslator
    if data.flags == 17:
      if data.vkCode == pynput.keyboard.Key.media_volume_up.value.vk:
        self.cir.send(Sony.VOL_UP)
        self.kb_listener.suppress_event()
        return False
      if data.vkCode == pynput.keyboard.Key.media_volume_down.value.vk:
        self.cir.send(Sony.VOL_DOWN)
        self.kb_listener.suppress_event()
        return False



    return True


  def kb_press(self, k):
    self.kb.press(k)
    self.kb.release(k)

  def handle(self, a, b, c=None):
    if b is None:
      return

    r = None
    try:
      r = self.mapping[a][b]
    except KeyError:
      pass

    # handle object
    if r:
      log.info((r, type(r)))
      if isinstance(r, Key):
        self.kb_press(r)
      if isinstance(r, pynput.keyboard.KeyCode):
        self.kb_press(r)
      elif isinstance(r, tuple):
        time.sleep(1)
        self.cir.send(r)
      else:
        log.warning('Unknown mapping: %r', r)
      return

    # handle function
    b = b.replace('.', '_')
    n = 'handle_{}_{}'.format(a, b)
    log.info(n)
    m = getattr(self, n, None)
    if m is None:
      log.warning('Unhandled: %s', n)
    else:
      m(c)

  def run(self):
    # pynput monitors run on their own threads
    self.kb_listener.start()
    self.kb_listener.wait()
    self.mouse_listener.start()
    self.mouse_listener.wait()

    # mainloop poll mcu and cli
    try:
      while 1:
        time.sleep(0.01)

        self.handle('cli', get_key())

        # Poll CIR
        if self.cir:
          line = self.cir.poll()
          if line is not None:
            if line.startswith('{'):
              try:
                data = json.loads(line)
                log.info(data)
                for k, v in data.items():
                    self.handle('cir', k, v)
              except json.decoder.JSONDecodeError as e:
                log.error('invalid json: %s\n%s', e, line)
            else:
              self.handle('ir', line)

        # Poll Keybow
        if self.keybow:
          cmd = self.keybow.poll()
          if cmd is not None:
            cmd = cmd.split()
            self.handle('keybow', cmd[0], cmd[1:])

    finally:
      self.kb_listener.stop()
      self.mouse_listener.stop()

  # def handle_cli_0d(self):
  #   # debug keypress
  #   def p(x):
  #     log.info('Key: %r %r', x, dir(x))
  #     try:
  #       log.info('Key: %r', x.vk)
  #     except: pass
  #   with pynput.keyboard.Listener(
  #       on_press=p,
  #       on_release=p) as l:
  #     time.sleep(1)
  #   l.join()

Key = pynput.keyboard.Key
Key.stop = pynput.keyboard.KeyCode(vk=178)

class KnioTranslator(Translator):
  mapping = {
    'ir': {
      # Amp
      'S.B0.78': Key.up,
      'S.B0.79': Key.down,
      'S.B0.7A': Key.left,
      'S.B0.7B': Key.right,
      'S.30.0C': Key.enter,
      'S.30.00': AC.POWER,

      # 'S.10.32.08': Key.media_play_pause,
      # 'S.10.39.08': Key.media_play_pause,
      # 'S.10.38.08': Key.stop,
      'S.10.2A.08': Key.stop,
      'S.10.34.08': Key.media_next,
      'S.10.33.08': Key.media_previous,
      'S.10.2F.08': pynput.keyboard.KeyCode(vk=183),
      'S.10.2E.08': pynput.keyboard.KeyCode.from_vk(182),
    }
  }
  FB2K = r'C:\Users\Tom\Desktop\Files\Software\foobar2000_151\foobar2000.exe'

  def __init__(self, *args, **kwargs):
    super(KnioTranslator, self).__init__(*args, **kwargs)
    self.projector_on = False

  def handle_cli_70(self,): # p
    self.cir.send(Sony.POWER)

  def handle_cli_71(self, data): # q
    return
    self.cir.ser.write('CO2_RESET\r'.encode('ascii'))
    self.cir.ser.flush()

  def handle_cli_6f(self, data): # o
    self.kb_press(pynput.keyboard.Key.media_play_pause)
    self.cir.send(Sony.INPUT_BD)
    self.cir.send(Projector.ON)

  def handle_cli_0d(self, data):
    if self.cir:
      self.cir.send(Light.ON)

  def handle_ir_S_01_15(self, data):
    # TV i/o
    if self.projector_on:
      time.sleep(1)
      self.cir.send(Projector.OFF)
      time.sleep(2)
      self.cir.send(Projector.OFF)
    else:
      time.sleep(1)
      self.cir.send(Projector.ON)
    self.projector_on = not self.projector_on

  def handle_ir_S_10_32_08(self, data):
    subprocess.check_call([self.FB2K, '/play'])

  def handle_ir_S_10_39_08(self, data):
    subprocess.check_call([self.FB2K, '/pause'])

  def handle_ir_S_10_38_08(self, data):
    subprocess.check_call([self.FB2K, '/stop'])

  def handle_keybow_fb2k(self, data):
    cmd = data[0]
    subprocess.check_call([self.FB2K, '/' + cmd])
    if self.cir:
      self.cir.send(Sony.INPUT_TV)

  def handle_keybow_light(self, data):
    cmd = data[0]
    if cmd == 'on':
      self.cir.send(Light.ON)
    if cmd == 'off':
      self.cir.send(Light.OFF)
    else:
      log.warning('Unknown keybow light command: %s', cmd)

  def handle_keybow_sony(self, data):
    cmd = data[0]
    if cmd == 'power':
      self.cir.send(Denon.POWER)
      time.sleep(1)
      self.cir.send(Sony.INPUT_TV)
    else:
      log.warning('Unknown keybow light command: %s', cmd)

  def handle_keybow_fan(self, data):
    cmd = data[0]
    if cmd == 'mode':
      self.cir.send(Fan.MODE)
    else:
      log.warning('Unknown keybow light command: %s', cmd)

  def handle_cir_PMS(self, data):
      post_grafana({
        f'pms.{k}':v for k,v in data.items()})

  def handle_cir_SCD30(self, data):
      post_grafana({
        f'scd.{k}':v for k,v in data.items()})



def main():
  ser1 = serial.Serial('COM17', timeout=0)
  c = CIR(ser1)
  # c = None

  # ser2 = serial.Serial('COM12',
  #   baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1)
  # w = Keybow(ser2)
  w = None
  m = None

  k = pynput.keyboard.Controller()
  # m = pynput.mouse.Controller()
  t = KnioTranslator(c, k, m, w)
  try:
    t.run()
  except KeyboardInterrupt:
    pass


if __name__ == '__main__':
  logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)s: %(message)s')

  logging.getLogger('urllib3').setLevel(logging.WARNING)

  main()

