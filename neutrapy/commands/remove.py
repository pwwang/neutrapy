from subprocess import Popen

import rtoml as toml

from ..utils import logh
from .sync import run as run_sync


def run(args):
    """Remove python dependencies from pyproject.toml and sync the neutrapy.toml
    """
    with open("neutrapy.toml") as f:
        config = toml.load(f)

    cmds = [config["python"], "-m", "poetry", "remove"]
    if args["dev"]:
        cmds.append("--dev")

    cmds.extend(args[""])

    logh("Running: poetry remove ...")
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
        sync_pypj=False,  # poetry remove already did this
        update_pylock=False,  # poetry remove already did this
    )
