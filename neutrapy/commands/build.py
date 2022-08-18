
import json
import sys
import shutil
from subprocess import Popen
from pathlib import Path

import rtoml as toml

from ..utils import backingup, logh


def run(args):
    """Build the project"""
    logh("Checking if downstream configuration files are up to date ...")
    npyfile = Path("neutrapy.toml")
    neufile = Path("neutralino.config.json")
    pypfile = Path("pyproject.toml")
    npy_mtime = npyfile.stat().st_mtime
    neu_mtime = neufile.stat().st_mtime
    pyp_mtime = pypfile.stat().st_mtime

    if (npy_mtime > neu_mtime or npy_mtime > pyp_mtime) and not args.force:
        print(
            "neutrapy.toml is newer than downstream configuration files, \n"
            "please run `neutrapy sync` first or pass `--force`."
        )
        sys.exit(0)

    with open(npyfile) as f:
        config = toml.load(f)

    logh("Building python extension into binary ...")
    cmds = [
        "pyoxidizer",
        "build",
        "--target-triple",
        config["target"],
        "--release",
    ]
    Popen(cmds).wait()

    logh("Backing up neutralino config file ...")
    with backingup(neufile):
        with open(neufile) as f:
            nconfig = json.load(f)

        logh("Modifying python extension command ...")
        nconfig["modes"]["window"]["enableInspector"] = False
        for extension in nconfig["extensions"]:
            if extension["id"].endswith(".python"):
                extension["command"] = str(Path("backend", "python"))

        with open(neufile, "w") as f:
            json.dump(nconfig, f, indent=4)

        logh("Building neutralino app ...")
        cmds = [shutil.which("neu"), "build"]
        Popen(cmds).wait()

        logh("Copying binary python extension into neutralino app ...")
        backend_dir = Path("dist").joinpath(config["name"], "backend")
        if backend_dir.exists():
            shutil.rmtree(backend_dir)
        shutil.copytree(
            Path("build").joinpath(config["target"], "release", "install"),
            Path("dist").joinpath(config["name"], "backend"),
        )

    logh("Copying neutrapy.toml ...")
    shutil.copy(
        npyfile,
        Path("dist").joinpath(config["name"], "neutrapy.toml"),
    )

    logh("Your app is built at ./dist")
