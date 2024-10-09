r'''

\\.\PhysicalDriveN
\\.\X:


'''

import argparse
import os
import sys
import logging
import treecat

import colorama


LOG = logging.getLogger('hdd')


def main(args):
  print(f'Opening: {args.path}')
  f = os.open(args.path,
    os.O_BINARY |
    os.O_RDONLY |
    # os.O_DIRECT |
    # os.O_DIRECTORY |
    0
  )
  data = os.read(f, 512)

  lines = treecat.treecat.xxd(data, 16)
  for i, d in lines:
    print(f'{i:03x} {d}', end='')



if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    level=logging.DEBUG,
  )

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)

  # do not use pathlib.Path here
  parser.add_argument('path', type=str)
  args = parser.parse_args()

  colorama.init()
  sys.stdout.reconfigure(encoding='utf8')

  main(args)
