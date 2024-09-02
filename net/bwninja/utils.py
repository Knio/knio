import os
import pathlib
import logging
import sys

LOG = logging.getLogger(__name__)



def get_import_paths(*modules):
  paths = set()
  for m in modules:
    paths.add(pathlib.Path(m.__file__).parent.parent)
  return list(map(str, paths))


def escalate(paths, *args):
  env = dict(
    PYTHONDONTWRITEBYTECODE='1',
    PYTHONPATH=':'.join(paths)
  )
  LOG.debug(env)

  argv = pathlib.Path('/proc/self/cmdline').read_text().split('\0')[1:-1]
  LOG.debug(argv)

  cmd = [
    'sudo', '-E',
    *[f"'{k}={v}'" for k, v in env.items()],
    sys.executable, *argv, *args,
  ]
  LOG.debug(cmd)
  os.execv('/usr/bin/sudo', cmd)

