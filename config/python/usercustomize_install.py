print("Installing usercustomize.py")

import pathlib
import site
import os

src = pathlib.Path(__file__).with_stem('usercustomize')
dst = pathlib.Path(site.getusersitepackages()) / src.name
print(f"Linking {dst} to {src}")
os.link(src, dst)
