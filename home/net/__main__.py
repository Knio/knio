import logging
import argparse

from . import net

def main():

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=__doc__)
  parser.add_argument('--interface', '-i', type=str, default='eth0')
  parser.add_argument('--interval', '-t', type=int, default=5)
  parser.add_argument('--attachment', '-a', type=str, default='socket')
  parser.add_argument('--db', type=str, default='netflow.db')
  parser.add_argument('--printk', default=False, action='store_true')

  args = parser.parse_args()
  net.run(vars(args))

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s')

  main()

