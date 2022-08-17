import shutil
from subprocess import Popen

from ..utils import logh


def _installed(binary):
    """Check if a binary is installed."""
    return shutil.which(binary) is not None

def run(args):
    """Check if neutralinocli and poetry are installed."""
    # check if neu is installed, this implictly checks if npm is installed
    if not _installed("neu") and not _installed("npx"):
        logh("x Neither `neu` or `npx` is not installed, please install it first.")
        print("  See: https://neutralino.js.org/docs/cli/neu-cli#installation")
    else:
        logh("✔ neu is installed.")

    rc = Popen([args.python, "-m", "poetry", "--version"]).wait()
    if rc != 0:
        logh("x `poetry` is not installed, please install it first.")
        print("  See: https://python-poetry.org/docs/#installation")
    else:
        logh(
            "✔ poetry is installed."
        )

    rc = Popen(["pyoxidizer", "--version"]).wait()
    if rc != 0:
        logh("x `pyoxidizer` is not installed, please install it first.")
        print(
            "  See: https://gregoryszorc.com/docs/pyoxidizer/main/"
            "pyoxidizer_getting_started.html#python-wheels"
        )
    else:
        logh(
            "✔ pyoxidizer is installed."
        )
