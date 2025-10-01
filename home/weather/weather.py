#! /usr/bin/python3
import json
import logging
import pathlib
import subprocess
import sys


home = pathlib.Path(__file__).parent.parent
sys.path.append(str(home))


import grafana

LOG = logging.getLogger('weather')



class LerpSet:
  def __init__(self, setpoints):
    pass

  def lerp(self, id, x):
    return x



def f_to_c(x):
  return (x - 32.) * 5. / 9.


def main():
  cmd = [
    'rtl_433',
      '-F', 'json',
      '-C', 'si',
      '-f', '433.926M',
      # '-Y', 'autolevel',
      # '-Y', 'minmax',
      # '-Y', 'magest',
      '-M', 'level',
      '-M', 'noise',
  ]
  LOG.info(f"cmd: {' '.join(cmd)}")
  rtl = subprocess.Popen(cmd, stdout=subprocess.PIPE)

  lerp = LerpSet(({
    'A': 18.83,
    'B': 18.89,
    'C': 18.94,
    'D': 18.83,
    'E': 18.79,
    'F': 18.88,
    'G': 18.84,
    },{
    'A': 48.14,
    'B': 48.44,
    'C': 48.53,
    'D': 48.33,
    'E': 48.72,
    'F': 48.32,
    'G': 48.16,
  }))


  def process(line):
    data = json.loads(line)
    line_s = line.decode('ascii').strip()
    if data.get('model') == 'Ambientweather-F007TH':
      id_ch_to_name = {
        # 1 bit = 0.056
        # Ch  ID   SID   Name
        (1,  61): ('A', 'Office'),
        (2,  89): ('B', ''),
        (3, 192): ('C', 'Attic'),
        (1, 247): ('D', 'Outside'),
        (2,   8): ('E', 'LivingRoom'),
        (3, 148): ('F', 'F'),
        (1, 175): ('G', 'Slab'),
      }
      ch_id = data.get('channel'), data.get('id')
      sid, name = id_ch_to_name.get(ch_id, (None, 'Unknown'))
      if sid is None:
        LOG.warning(f'\n\nUnknown sensor: {line_s}\n\n')
        return
      LOG.info(f'{name:<12s} {line_s}')

      rt = data['temperature_C']
      rh = data['humidity']

      ct = lerp.lerp(sid, rt)
      # ch = lerp.lerp(sid, rh)
      ch = rh

      grafana.post('rtl',
        interval=300,
        **{
          f'Temperature_{name}': ct,
          f'Humidity_{name}': ch,
        }
      )

    else:
      LOG.warning(f'\n\nUnknown sensor: {line}\n\n')

  try:
    for line in rtl.stdout:
      process(line)
    if rtl.wait() != 0:
      print('''
  To proxy usb to WSL2:
  usbipd wsl attach  -b 11-4 -d Ubuntu-20.04
  ''')

  except KeyboardInterrupt:
    # rtl.send_signal(2)
    return



if __name__ == '__main__':
  logging.basicConfig(
    level=logging.DEBUG,
    datefmt='%y%m%d-%H%M%S',
    format='%(asctime)s:%(levelname)s:%(filename)s:%(lineno)s:%(funcName)s: %(message)s')

  logging.getLogger('urllib3').setLevel(logging.WARNING)

  main()
