import argparse
import concurrent.futures
import datetime
import itertools
import json
import multiprocessing as mp
import pathlib
import pprint
import queue
import random
import subprocess
import threading
import time
from dataclasses import dataclass

import ultralytics
import ephem
import pytz


FFMPEG = pathlib.Path(r"~/bin/ffmpeg-prebuilt/ffmpeg")
MODEL = "birb-2024-07-26.pt"

class Seg(pathlib.Path):
  def json(self):
    return self.with_suffix('.json')

  def detections(self):
    j = self.json()
    if j.is_file():
      return json.loads(j.read_text())
    print(f'DETECT START {self}')
    # re-create MODEL for thread safety
    model = ultralytics.YOLO(MODEL)
    results = model(self, vid_stride=15, stream=True)
    boxes = [r.summary() for r in results]
    j.write_text(json.dumps(boxes, sort_keys=True, indent=2))
    print(f'DETECT END {self}')
    return boxes

  def seconds(self):
    def filter(d):
      x = set()
      for box in d:
        n = box['name']
        c = box['confidence']
        # if c < thresholds.get(n, 0.2): continue
        if not (n in {'bird', 'cat','dog', 'bear'}):
          continue
        if c < 0.4:
          continue
        x.add(n)
      return x

    return [filter(d) for d in self.detections()]


  def cuts(self):
    sss = list(self.seconds())
    #  +/- 1s
    for i, s in enumerate(sss):
      if i > 0: sss[i - 1] |= s
    for i, s in reversed(list(enumerate(sss))):
      if i < len(sss) - 1: sss[i + 1] |= s

    current = None
    for i, s in enumerate(sss):
      ss = bool(s)
      if (current is None) or (current.selected != ss):
        next = Cut(start=i, selected=ss, seg=self, reason=s)
        if current:
          yield current
        current = next
      current.length += 1
    current.reason |= s
    yield current


@dataclass
class Cut:
  seg: Seg
  start: int
  selected: bool
  reason: set
  length: int = 0


def encode(args, data):
  out = args.root.parent / f'{args.root.name}.mp4'
  if args.suffix:
    out = out.with_stem(out.stem + '.' + args.suffix)
  out_timelapse = out.with_stem(out.stem + '.timelapse')
  encoder = subprocess.Popen(cmd := [
    FFMPEG,
    # input
    '-f', 'nut',
    '-r', '60',
    '-i',
      'pipe:0',
    '-an',

    # encoder
    '-codec:v', 'libx264',
      '-pix_fmt', 'yuv420p',
      '-profile:v', 'high',
      '-preset', 'medium',
      '-crf', '22',
      '-movflags', '+faststart',

    # output
    '-y', out,

    # out
    '-vf', 'framestep=5,setpts=PTS/5,fps=60',
    '-y', out_timelapse,
    ],
    stdin=subprocess.PIPE,
    # stderr=subprocess.DEVNULL,
  )
  print('  '.join(repr(str(c)) for c in cmd))
  for bytes in data:
    while bytes:
      n = encoder.stdin.write(bytes)
      bytes = bytes[n:]
  encoder.stdin.close()
  encoder.wait(300)
  assert encoder.returncode == 0, encoder.returncode


def decode(cut, counter=[0]):
  drawtext = dict(
    box=1,
    boxcolor='#00000080',
    boxborderw=10,
    fontcolor='#808080',
    fontfile='/Windows/fonts/calibri.ttf',
    fontsize=72,
    text=' '.join(cut.reason),
    x='(128*3)',
    y='(h-32-text_h)',
  )

  print(f'piping {cut}')
  cmd = [
    FFMPEG,
  ]

  counter[0] += 1
  if 1 or counter[0] & 1:
    cmd += [
        # decoder
      '-hwaccel', 'nvdec',
    ]
  cmd += [
    # cut
    '-ss', f'{cut.start}',
    '-t', f'{cut.length}',
    # input
    '-i', cut.seg,
    '-an',

    # filters
    '-vf', f'framestep={"1" if cut.selected else "30"}'
      # ',drawtext=' +
      # ':'.join(f'{k}={v}' for k,v in drawtext.items()),
,
    # encoder
    '-codec:v', 'rawvideo',

    # output
    '-f', 'nut',
    'pipe:1',
  ]
  decoder = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
  )
  print(f'FFMPEG PID: {decoder.pid} START ' + '  '.join(repr(str(c)) for c in cmd))
  while 1:
    bytes = decoder.stdout.read(256 * 1024 ** 2)
    if not bytes:
      if decoder.poll() is not None:
        break
    # print(f'\ncopying {len(bytes)} bytes')
    yield bytes
  print(f'FFMPEG PID: {decoder.pid} DONE')
  assert decoder.returncode == 0, decoder.returncode


def iter_thread_producer(input, size=1, process=False):
  '''puts the input iterator in its own thread'''
  if process:
    q = mp.Queue(maxsize=size)
  else:
    q = queue.Queue(maxsize=size)

  def produce():
    for i in input:
      q.put(i)

  if process:
    producer = mp.Process(target=produce)
  else:
    producer = threading.Thread(target=produce)
  producer.daemon = True
  producer.start()

  def consume():
    while producer.is_alive():
      try:
        if not q.qsize():
          print(f'{input} producer is not keeping up')
        yield q.get(timeout=10)
      except queue.Empty:
        print(f'\nq timeout')
    while q.qsize():
      yield q.get_nowait()

  return consume()


def parallel_gens(iters, size):
  '''for generators that yield generators'''
  def consume():
    for iter in iters:
      yield iter_thread_producer(iter)
  return iter_thread_producer(consume(), size=size)


def flatten(iter):
  for i in iter:
    yield from i


def sun_times(date):
  localtz = pytz.timezone('US/Pacific')
  dt_naive = datetime.datetime.strptime(date, '%Y-%m-%d')
  dt_local = localtz.localize(dt_naive)
  dt_utc = dt_local.astimezone(datetime.timezone.utc)

  print(
    f'naive: {dt_naive}\n'
    f'local: {dt_local}\n'
    f'utc:   {dt_utc}\n'
  )

  obs = ephem.Observer()
  obs.lon = '-122.020545' # must be strings lol
  obs.lat = '37.297260'
  obs.date = dt_utc
  sun = ephem.Sun()
  # time is 00:00
  sunrise = obs.next_rising(sun)
  sunset = obs.next_setting(sun)
  return (
    ephem.localtime(sunrise),
    ephem.localtime(sunset)
  )


def dir_daylight_wait(root: pathlib.Path):
  sr, ss = sun_times(root.name)
  print(f'sunrise: {sr}, sunset: {ss}')
  et = datetime.timedelta(minutes=30)
  done = set()
  while 1:
    files = list(root.glob('birbs_*.mp4'))
    for f in sorted(files)[:-2]:
      if f in done:
        continue
      tm = datetime.datetime.strptime(f.stem, 'birbs_%Y%m%d-%H%M')
      if tm < sr - et:
        print(f'skipping before sunrise {f}')
        done.add(f)
        continue
      if tm > ss + et:
        print(f'stopping after sunset {f}')
        return # done!

      print(f'adding {f}')
      done.add(f)
      yield f

    print('waiting for more files...')
    time.sleep(10)


def cat_dir(args):
  # files = list(args.root.glob("birbs_*.mp4"))
  files = dir_daylight_wait(args.root)
  cuts = map(lambda f:Seg(f).cuts(), files)
  cuts = flatten(parallel_gens(cuts, size=6))
  framegens = map(decode, cuts)
  # framegens = parallel_gens(framegens, size=4) ### something broken
  frames = flatten(framegens)
  encode(args, frames)

  # TODO:
  # https://github.com/davidrazmadzeExtra/YouTube_Python3_Upload_Video/blob/main/upload_video.py
  # python3 upload_video.py --file="example.mov" --title="Summer vacation in California" --description="Had fun surfing in Santa Cruz" --keywords="surfing,Santa Cruz" --category="22" --privacyStatus="private"




def main(args):
  print('Hello, World!')
  cat_dir(args)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=__doc__,
  )
  parser.add_argument('root', type=pathlib.Path)
  parser.add_argument('--suffix', type=str, default=False)
  args = parser.parse_args()
  main(args)


