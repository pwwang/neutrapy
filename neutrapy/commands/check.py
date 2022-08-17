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

    p = Popen([args.python, "--version"]).communicate()
    if p.returncode != 0:
        print("x `poetry` is not installed, please install it first.")
        print("  See: https://python-poetry.org/docs/#installation")
    else:
        print(
            "✔ poetry is installed."
        )
