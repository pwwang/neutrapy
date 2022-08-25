import shutil
import warnings
from time import sleep
from pathlib import Path
from subprocess import Popen


def run(args):
    """Run the project"""

    dev_server = None
    cmds = [shutil.which("neu"), "run"]

    if args["disable-auto-reload"]:
        cmds.append("--disable-auto-reload")

    if args["frontend-lib-dev"]:
        cmds.append("--frontend-lib-dev")
        dev_server = Popen([shutil.which("npm"), "run", "dev"])
    elif Path("package.json").is_file():
        warnings.warn(
            "packages.json detected, "
            "do you mean to run with `--frontend-lib-dev`?"
        )

    if args["-"]:
        cmds.append("--")
        cmds.extend(args["-"])

    Popen(cmds).wait()
    if dev_server:
        dev_server.kill()
