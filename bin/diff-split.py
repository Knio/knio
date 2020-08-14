#! /usr/bin/env python3

import argparse
import copy
# import curses

import termios
import os
import tty
import logging
import subprocess
import sys
from collections import defaultdict

import unidiff
import colorama
import pygments.lexers
import pygments.formatters
# terminal256

CLEAR_SCREEN = '\x1b[2J'
KEY_LEFT = b'\x1b[D'
KEY_RIGHT = b'\x1b[C'




def interact(hunks):
  n = len(hunks)
  output = {}
  def next_unmarked():
    try:
      return next(i for i in range(n) if output.get(i) is None)
    except StopIteration:
      return 0

  def display(i):
    patched_file, hunk = hunks[i]
    o = output.get(i, None)

    patched_file_copy = copy.deepcopy(patched_file)
    patched_file_copy[:] = []
    text = '\n'.join([
        str(patched_file_copy),
        str(hunk),
    ])

    lexer = pygments.lexers.get_lexer_by_name('diff')
    formatter = pygments.formatters.Terminal256Formatter()
    colored_text = pygments.highlight(text, lexer, formatter)

    print(CLEAR_SCREEN)
    print(colored_text)

    if o == None:
      print(colorama.Back.RED)
      print('Hunk {}/{}      Unselected'.format(i + 1, n))
    else:
      print(colorama.Back.BLUE)
      print('Hunk {}/{}      Current output selection: {}'.format(i + 1, n, o))
    print(colorama.Back.RESET)

  i = 0
  while len(output) != n:
    display(i)
    c = sys.stdin.buffer.raw.read(3)
    if c == KEY_RIGHT:
      i = (i + 1) % n
    elif c == KEY_LEFT:
      i = (i - 1 + n) % n
    elif c == b'\n':
      i = next_unmarked()
    elif c == b'q':
      break
    elif c in b'123456789':
      output[i] = int(c)
      i = next_unmarked()
    else:
      raise Exception('Unhandled keypress', repr(c))
  print(CLEAR_SCREEN)
  return output


def load_hunks(diffs):
  for diff in diffs:
    patch = unidiff.PatchSet(diff)
    for patched_file in patch:
      for hunk in patched_file:
        yield patched_file, hunk



def main():
  logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(asctime)s %(name)s: %(message)s')
  parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument('inputs',
    help="input diffs to load ('-' for stdin).\
      If omitted, will read from: \
        (1) git diff,\
        (2) git show \
      in sequence until an input is found",
    nargs='*')

  args = parser.parse_args()

  diffs = []
  for i in args.inputs:
    if i == '-':
      diffs.append(sys.stdin.read())
    else:
      diffs.append(open(i).read())

  git_diff = subprocess.check_output(['git','diff','--color=never'])
  if (not diffs) and git_diff:
    diffs.append(git_diff.decode('utf8'))

  git_show = subprocess.check_output(['git','show','--color=never'])
  if (not diffs) and git_show:
    diffs.append(git_show.decode('utf8'))

  if not diffs:
    raise Exception('No input found')

  hunks = list(load_hunks(diffs))
  n = len(hunks)
  if not n:
    raise Exception('Failed to load any hunks')

  orig_term = termios.tcgetattr(sys.stdin)
  new_term = list(orig_term)
  new_term[3] &= ~(termios.ECHO | termios.ICANON)
  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_term)
  try:
    output = interact(hunks)
  finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_term)

  outputs = sorted(set(output.values()))
  for o in outputs:
    hunk_set = [hunks[i] for i in range(n) if output.get(i) == o]
    files = {}
    for patched_file, hunk in hunk_set:
      if not id(patched_file) in files:
        patched_file_copy = copy.deepcopy(patched_file)
        patched_file_copy[:] = []
        files[id(patched_file)] = patched_file_copy
      files[id(patched_file)].append(hunk)

    patch = unidiff.PatchSet('')
    patch.extend(files.values())
    fname = 'patch_{}.diff'.format(o)
    open(fname, 'w').write(str(patch))
    print('Wrote {}'.format(fname))


if __name__ == '__main__':
  main()
