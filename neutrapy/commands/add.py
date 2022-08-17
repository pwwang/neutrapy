from subprocess import Popen

import rtoml as toml

from ..utils import logh
from .sync import run as run_sync


def run(args):
    """Add python dependencies to pyproject.toml and sync the neutrapy.toml"""
    with open("neutrapy.toml") as f:
        config = toml.load(f)

    cmds = [config["python"], "-m", "poetry", "add"]
    if args["dev"]:
        cmds.append("--dev")
    if args["extras"]:
        cmds.extend(["--extras", *args["extras"]])
    if args["optional"]:
        cmds.append("--optional")
    if args["pyver"]:
        cmds.extend(["--python", args["pyver"]])
    if args["platform"]:
        cmds.extend(["--platform", args["platform"]])
    if args["source"]:
        cmds.extend(["--source", args["source"]])
    if args["allow-prereleases"]:
        cmds.append("--allow-prereleases")
    if args["lock"]:
        cmds.append("--lock")

    cmds.extend(args[""])

    logh("Running: poetry add ...")
    Popen(cmds).wait()

    logh("Syncing to neutrapy.toml ...")
    with open("pyproject.toml") as f:
        pyproject = toml.load(f)
    with open("neutrapy.toml") as f:
        neutrapy = toml.load(f)

    neutrapy["poetry"]["tool"]["poetry"]["dependencies"] = (
        pyproject["tool"]["poetry"]["dependencies"]
    )
    neutrapy["poetry"]["tool"]["poetry"]["dev-dependencies"] = (
        pyproject["tool"]["poetry"]["dev-dependencies"]
    )
    with open("neutrapy.toml", "w") as f:
        toml.dump(neutrapy, f)

    logh("Syncing to downstream files ...")
    run_sync(
        {},
        sync_pypj=False,  # poetry add already did this
        update_pylock=False,  # poetry add already did this
    )
