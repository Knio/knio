'''
Backs up from a remote source to a local target.
'''

import os
import pathlib
import subprocess
import logging
import typing


LOG = logging.getLogger()

class B(typing.NamedTuple):
  target_root: pathlib.Path
  source_host: str
  source: pathlib.Path



DST = 'zp_backup'

'''
Initial setup:

sudo zfs set canmount=noauto zp_backup_6tb
sudo zfs allow tom create,receive,mount zp_backup_6tb
'''


CONFIG = [
  B(DST, 'truenas', 'zp/tom/home'),
  B(DST, 'truenas', 'zp/tom/docs'),
  B(DST, 'truenas', 'zp/tom/archive'),
  B(DST, 'truenas', 'zp/tom/software'),
  B(DST, 'truenas', 'zp/tom/photos'),
  B(DST, 'truenas', 'zp/erin'),
  B(DST, 'truenas', 'zp/tom/pics'),
]


def get_snapshots(name, host=None):
  class Snapshot(typing.NamedTuple):
    name: pathlib.Path
    size: int
  if host:
    cmd = ['ssh', host]
  else:
    cmd = []
  out = subprocess.check_output(cmd + [
    'zfs', 'list',
    '-H', '-p',
    '-t', 'snapshot',
    '-o', 'name,used',
    '-s', 'createtxg',
    str(name)
  ], encoding='utf8')


  def ss(line):
    fqn, size = line.split('\t', 1)
    # pool, fs = fqn.split('/', 1)
    return Snapshot(pathlib.Path(fqn), int(size))
  return [ss(line) for line in out.splitlines()]


def send_recv(dst_root, src_host, src, src_inc=None):
  pipe = os.pipe2(os.O_CLOEXEC)
  inc = []
  if src_inc:
    inc = ['-i', src_inc]
  send = subprocess.Popen([
    'ssh', src_host,
    'zfs', 'send',
    '--raw', '--replicate',
    '-v', # TODO use SIGUSR1 instead to generate progress logs
    str(src)
  ] + inc, stdin=subprocess.DEVNULL, stdout=pipe[1])
  recv = subprocess.Popen([
    'zfs', 'receive', '-v', '-d', str(dst_root)
  ], stdin=pipe[0])
  if recv.wait() != 0:
    raise ValueError(recv.returncode)
  if send.wait() != 0:
    raise ValueError(send.returncode)


def main():
  for b in CONFIG:
    LOG.info(f'Backing up {b.target_root} 🡸  {b.source_host}:{b.source}')
    dst_root = pathlib.Path(b.target_root)
    src_pool, src_name = b.source.split('/', 1)
    src_pool = pathlib.Path(src_pool)
    src_name = pathlib.Path(src_name)

    they_have = get_snapshots(src_pool / src_name, host=b.source_host)
    try:
      we_have =   get_snapshots(dst_root / src_name)
    except subprocess.CalledProcessError as e:
      print(e)
      if 'y' == input('Could not get local snapshots. This could mean the filesystem does not exist yet. Continue? [y/n]: '):
        we_have = []
      else:
        raise

    we_have_ss = set(x.name.relative_to(dst_root) for x in we_have)

    last = None
    for ss in they_have:
      no = ss.name.relative_to(src_pool)

      sz = f'({ss.size/1024**2:,.2f} MiB)'
      if no in we_have_ss:
        LOG.info(f'Already have {no} {sz}, skipping')
        last = no
        continue
      iss = None
      if last:
        iss = str(last).rsplit('@', 1)[1]
      # TODO: if we have some non-contiguous snapshots, this will fail.
      # we should instead skip ahead to the last one we have
      LOG.info(f'Copying {no} {sz}')
      send_recv(dst_root, b.source_host, ss.name, iss)
      last = no


if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    datefmt='%y%m%d-%H%M%S',
    level=logging.INFO,
  )
  main()
