import sys
import pathlib

_bin = pathlib.Path(__file__).parent.parent.parent/'bin'
sys.path.append(str(_bin))
import datum
