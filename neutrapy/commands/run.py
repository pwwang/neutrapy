import shutil
import shlex
from subprocess import Popen

from pyparam import POSITIONAL


def run(args):
    """Run the project"""
    cmds = [shutil.which("neu"), "run"]
    if args["disable-auto-reload"]:
        cmds.append("--disable-auto-reload")
    if args["frontend-lib-dev"]:
        cmds.append("--frontend-lib-dev")
    if args[POSITIONAL]:
        cmds.append("--")
        cmds.extend(shlex.split(args[POSITIONAL]))

    Popen(cmds).wait()
