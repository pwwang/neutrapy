import shutil
from subprocess import Popen


def _installed(binary):
    """Check if a binary is installed."""
    return shutil.which(binary) is not None

def run(args):
    """Check if neutralinocli and poetry are installed."""
    # check if neu is installed, this implictly checks if npm is installed
    if not _installed("neu") and not _installed("npx"):
        print("x Neither `neu` or `npx` is not installed, please install it first.")
        print("  See: https://neutralino.js.org/docs/cli/neu-cli#installation")
    else:
        print("✔ neu is installed.")

    rc = Popen([args.python, "-m", "poetry", "--version"]).wait()
    if rc != 0:
        print("x `poetry` is not installed, please install it first.")
        print("  See: https://python-poetry.org/docs/#installation")
    else:
        print(
            "✔ poetry is installed."
        )

    rc = Popen(["pyoxidizer", "--version"]).wait()
    if rc != 0:
        print("x `pyoxidizer` is not installed, please install it first.")
        print(
            "  See: https://gregoryszorc.com/docs/pyoxidizer/main/"
            "pyoxidizer_getting_started.html#python-wheels"
        )
    else:
        print(
            "✔ pyoxidizer is installed."
        )
