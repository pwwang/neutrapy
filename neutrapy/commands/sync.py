import json
from pathlib import Path
from subprocess import Popen

import rtoml as toml

from ..utils import logh, replace_placeholders, get_python_version


def run(
    args,
    sync_pypj=True,
    update_pylock=True,
    sync_neu=True,
):
    """Sync neutrapy.toml to downstream configuration files"""
    with open("neutrapy.toml") as f:
        config = toml.load(f)

    data = {
        key: val
        for key, val in config.items()
        if key not in ("neutralino", "poetry")
    }
    data["pyver"] = get_python_version(config["python"])
    data["pyminorver"] = get_python_version(config["python"], 2)

    if sync_pypj:
        logh("Syncing to pyproject.toml ...")
        pypj = toml.dumps(config["poetry"])
        with open("pyproject.toml", "w") as f:
            f.write(replace_placeholders(pypj, **data))

    if sync_neu:
        logh("Syncing to neutralino.config.json ...")
        neu = json.dumps(config["neutralino"], indent=4)
        with open("neutralino.config.json", "w") as f:
            # escape the python path on windows
            f.write(
                replace_placeholders(
                    neu,
                    python=data["python"].replace("\\", "\\\\"),
                    **{k: v for k, v in data.items() if k != "python"}
                )
            )

    if update_pylock:
        logh("Updating pyproject.lock ...")
        cmds = [data["python"], "-m", "poetry", "update"]
        Popen(cmds).wait()

    logh("Updating requirements.txt ...")
    cmds = [
        config["python"],
        "-m",
        "poetry",
        "export",
        "-f",
        "requirements.txt",
        "-o",
        "requirements.txt",
    ]
    Popen(cmds).wait()

    logh("Updating pyoxidizer.bzl ...")
    pyox = Path("pyoxidizer.bzl").read_text()
    pyox = replace_placeholders(pyox, **data)
    Path("pyoxidizer.bzl").write_text(pyox)
