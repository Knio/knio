import sys
import pathlib

#                             devices/ home/ knio/
_bin = pathlib.Path(__file__).parent.parent.parent
sys.path.append(str(_bin))
import datum
