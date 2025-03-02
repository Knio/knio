
import argparse
import logging


from bcc import BPF, USDT, StrcmpRewrite

log = logging.getLogger('portmap' if __name__ == '__main__' else __name__)


def run(args):
  bpf = BPF(src_file='portmap.c', cflags=['-O2', '-Wall'])
  bpf.attach_xdp(
    dev='wg0',
    fn=bpf.load_func('trace_udp_sendmsg', BPF.XDP),
    flags=0)

  bpf.attach_kprobe(event='udp_sendmsg', fn_name='trace_udp_sendmsg')

  log.info("Running")
  while 1:
    try:
      bpf.perf_buffer_poll()
    except KeyboardInterrupt:
      break
  log.info("Exiting")



def main():
  parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
  )

  args = parser.parse_args()
  run(args)


if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  main()
