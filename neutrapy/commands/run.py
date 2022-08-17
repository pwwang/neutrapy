import shutil
from subprocess import Popen


def run(args):
    """Run the project"""
    cmds = [shutil.which("neu"), "run"]
    if args["disable-auto-reload"]:
        cmds.append("--disable-auto-reload")
    if args["frontend-lib-dev"]:
        cmds.append("--frontend-lib-dev")
    if args["-"]:
        cmds.append("--")
        cmds.extend(args["-"])

    Popen(cmds).wait()
