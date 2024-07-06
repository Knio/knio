import argparse
import pathlib
import datetime


def main(args):
  d = datetime.date.today()
  for i in range(60):
    f = d.isoformat()
    print(f)
    p = args.root / f
    p.mkdir(exist_ok=True, parents=True)
    d += datetime.timedelta(days=1)



if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=__doc__,
  )
  parser.add_argument('root', type=pathlib.Path)
  args = parser.parse_args()
  main(args)
