print("Installing usercustomize.py")

import pathlib
import shutil
import site
import os
import sys

src = pathlib.Path(__file__).with_stem('usercustomize').resolve()
dst = pathlib.Path(site.getusersitepackages()) / src.name

if dst.is_symlink():
  print(f'{dst} is already a link to {dst.readlink()}, not linking')
  sys.exit(-1)

dst.parent.mkdir(exist_ok=True, parents=True)

print(f"Linking {dst} to {src}")


if sys.platform == 'win32':
  shutil.copy(src, dst)
else:
  os.link(src, dst)
