
import argparse
import glob
import logging
from datetime import datetime, timedelta
import pathlib
import re
import subprocess
import tempfile


LOG = logging.getLogger('ff-cat')



def main(args):

  if not args.start:
    now = datetime.now()
    H = 6
    x = now.hour % H
    end = now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=x)
    start = end - timedelta(hours=H)
    LOG.debug(f'{now=}, {x=}, {start=}, {end=}')
  else:
    start = datetime.strptime(args.start, '%Y%m%d-%H')
    end = start + timedelta(hours=6)

  input_files = sorted(args.dir.glob('*.mp4'))
  cat = []
  name = None
  for f in input_files:
    if not (m := re.match(r'^(.+)\.(\d{8}-\d{4})\.mp4$', f.name)):
      LOG.debug(f'Skipping file with unexpected name: {f}')
      continue
    if name and m.group(1) != name:
      LOG.debug(f'Skipping file with different name: {f}')
      continue
    name = m.group(1)
    dt_str = m.group(2)
    dt = datetime.strptime(dt_str, '%Y%m%d-%H%M')
    if (start <= dt < end):
      cat.append(f)

  if cat and cat[-1] == f:
    LOG.error(f'Last file {f} may be incomplete')
    raise SystemExit(1)

  if not cat:
    LOG.info('No files to concatenate')
    raise SystemExit(2)

  out = cat[0].with_name(f'{name}.{start.strftime("%Y%m%d-%H")}.mp4')

  flist = tempfile.NamedTemporaryFile(
    mode='w', delete=True, prefix='ffmpeg-concat-', suffix='.txt')
  for f in cat:
    flist.write(f"file '{f.resolve()}'\n")
  flist.flush()

  ls = "\n\t".join(map(str, cat))
  LOG.debug(f'Files to concatenate: \n\t{ls}')
  subprocess.check_call([
    'ffmpeg',
    '-f', 'concat',
    '-safe', '0',
    '-i', flist.name,
    '-c', 'copy',
    '-map_metadata', '0',
    '-movflags', '+faststart+global_sidx',
    out.resolve(),
  ])

  if args.delete:
    for f in cat:
      LOG.debug(f'Deleting input file: {f.resolve()}')
      f.unlink()

  LOG.info(f'Wrote output file: {out.resolve()}')


if __name__ == "__main__":
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    level=logging.INFO,
  )

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)
  parser.add_argument('dir', type=pathlib.Path, default=pathlib.Path('.'),
      help='Directory with input files')
  parser.add_argument('start', nargs='?',
      help='Start time in format YYYYMMDD-HH (e.g., 202406-12')
  parser.add_argument('--delete', action='store_true', default=False,
      help='Delete input files after concatenation')

  args = parser.parse_args()
  main(args)
