import time
import argparse
import pathlib
import subprocess
import itertools
import pprint
import json
import queue
import threading
import random
import concurrent.futures
import multiprocessing as mp
from dataclasses import dataclass

import ultralytics


TMP = pathlib.Path(r"c:\Temp")
ROOT = pathlib.Path(r"F:\Temp\birbs")
FFMPEG = pathlib.Path(r"C:\Users\Tom\Desktop\Files\Software\FFmpeg\ffmpeg-7.0.1-full_build\bin\ffmpeg.exe")
MODEL = ultralytics.YOLO("yolov10s.pt")


class Seg(pathlib.Path):
  def json(self):
    return self.with_suffix('.json')

  def small(self):
    out = self.with_stem(self.stem + '.small')
    out = TMP / out.name
    if out.is_file(): return out
    subprocess.check_call([
      FFMPEG,
      '-i', self,
      '-vf', 'fps=1 , scale=640:-1',
      out
    ])
    return out

  def detections(self):
    j = self.json()
    if j.is_file():
      return json.loads(j.read_text())
    print(f'DETECT START {self}')

    classes = set(range(1024))
    classes -= {
      47, # apple
      49, # orange
      56, # chair
      58, # potted plant
      25, # umbrella
      75, # vase
      32, # sports ball
      13, # bench
      60, # dining table
      8, # boat
    }
    # print(classes)
    # re-create MODEL for thread safety
    model = ultralytics.YOLO("yolov10s.pt")
    results = model(self, vid_stride=15, classes=list(classes), stream=True)
    boxes = [r.summary() for r in results]
    j.write_text(json.dumps(boxes, sort_keys=True, indent=2))
    print(f'DETECT END {self}')
    return boxes

  def seconds(self):
    thresholds = dict(
      person=2,
      car=2,
      chair=2,
      orange=2,
      apple=2,
      umbrella=2,
      vase=2,
      bench=2,
      boat=2,
      train=2,
      bicycle=2,
      cow=2,
      donut=2,
      clock=2,
      sandwich=2,
      skis=2,
      airplane=2,
    )
    thresholds['potted plant'] = 2
    thresholds['sports ball'] = 2
    thresholds['dining table'] = 2
    thresholds['stop sign'] = 2

    def take(d):
      x = set()
      for box in d:
        n = box['name']
        c = box['confidence']
        if c < thresholds.get(n, 0.2): continue
        x.add(n)
      return x

    cuts = [take(d) for d in self.detections()]
    return cuts


  def cuts(self):
    sss = list(self.seconds())
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


def encode(out, data):
  encoder = subprocess.Popen(cmd := [
    FFMPEG,
    # input
    '-f', 'nut',
    '-r', '15',
    '-i', 'pipe:0',
    '-an',

    # encoder
    '-codec:v', 'libx264',
      '-profile:v', 'high',
      '-preset', 'medium',
      '-crf', '24',
      '-movflags', '+faststart',

    # output
    '-y',
    out,
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
  encoder.wait(60)
  assert encoder.returncode == 0, encoder.returncode


def decode_cut(cut, counter=[0]):
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
  if counter[0] & 1:
    cmd += [
        # decoder
      # '-hwaccel', 'nvdec',
    ]
  cmd += [
    # cut
    '-ss', f'{cut.start}',
    '-t', f'{cut.length}',
    # input
    '-i', cut.seg,
    '-an',

    # filters
    '-vf', f'fps=fps={"15" if cut.selected else "0.125"}'
      ',drawtext=' +
      ':'.join(f'{k}={v}' for k,v in drawtext.items()),

    # encoder
    '-codec:v', 'rawvideo',

    # output
    # '-r', '15',
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


def iter_thread_producer(input, size=10, process=False):
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


def parallel_gens(iters, size=4, process=False):
  '''for generators that yield generators'''
  def consume():
    for iter in iters:
      yield iter_thread_producer(iter, process=process)
  return iter_thread_producer(consume(), size=size)


def flatten(iter):
  for i in iter:
    yield from i


def cat_dir(root):
  files = list(root.glob("*.mp4"))
  cuts = map(lambda f:Seg(f).cuts(), files)
  cuts = flatten(parallel_gens(cuts))
  framegens = map(decode_cut, cuts)
  # frames = flatten(parallel_gens(framegens, size=4))
  frames = flatten(framegens)
  encode(root.parent / f'{root.name}.mp4', frames)
  # TODO:
  # https://github.com/davidrazmadzeExtra/YouTube_Python3_Upload_Video/blob/main/upload_video.py
  # python3 upload_video.py --file="example.mov" --title="Summer vacation in California" --description="Had fun surfing in Santa Cruz" --keywords="surfing,Santa Cruz" --category="22" --privacyStatus="private"




def main(args):
  print('Hello, World!')
  cat_dir(args.root)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=__doc__,
  )
  parser.add_argument('root', type=pathlib.Path)
  args = parser.parse_args()
  main(args)


