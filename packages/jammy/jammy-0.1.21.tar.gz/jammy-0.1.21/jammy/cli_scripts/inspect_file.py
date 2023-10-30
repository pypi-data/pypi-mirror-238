# pylint: skip-file
import jammy
from jammy import *
from jammy import io as jio

parser = jammy.cli.JamArgumentParser()
parser.add_argument("filename", nargs="+")
args = parser.parse_args()


def simple():
    for i, filename in enumerate(args.filename):
        globals()[f"f{i + 1}"] = jio.load(filename)

    from IPython import embed

    embed()
