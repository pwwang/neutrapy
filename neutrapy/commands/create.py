import sys
import json
import shutil
from platform import python_version
from subprocess import Popen

import rtoml as toml
from pathlib import Path

from .. import current_platform_rs

TPL_DIR = Path(__file__).parent.parent.joinpath("templates")


def replace_placeholders(config, **values):
    if isinstance(config, str):
        config_str = config
    else:
        config_str = json.dumps(config, indent=4)

    for key, value in values.items():
        config_str = config_str.replace(f"${{{key}}}", str(value))

    if isinstance(config, str):
        return config_str

    return json.loads(config_str)


def run(args):
    """Create a new project"""
    target = current_platform_rs.platform()
    workdir = Path.cwd().joinpath(args.name)
    pyver = python_version()
    pyminorver = ".".join(pyver.split(".")[:2])
    if workdir.exists() and not args.force:
        raise FileExistsError(
            f"Directory `{workdir}` already exists, "
            "try --force to overwrite it."
        )

    if workdir.is_dir():
        print("- Removing existing project directory ...")
        shutil.rmtree(workdir)

    print("- Creating neutralinojs project ...")
    Popen([shutil.which("neu"), "create", args.name]).wait()

    print("- Copying template files ...")
    basedir = TPL_DIR.joinpath("default")
    tpldir = TPL_DIR.joinpath(args.template)
    for bfile in basedir.glob("**/*"):
        if bfile.is_dir():
            (
                workdir
                .joinpath(bfile.relative_to(basedir))
                .mkdir(parents=True, exist_ok=True)
            )
            continue

        tfile = tpldir.joinpath(bfile.relative_to(basedir))
        if not tfile.exists():
            tfile = bfile

        content = tfile.read_text()
        content = replace_placeholders(
            content,
            name=args.name,
            version=args.version,
            description=args.description,
            license=args.license,
            target=target,
            python=Path(args.python).as_posix(),
            python_version=pyver,
            python_minor_version=pyminorver,
        )
        workdir.joinpath(bfile.relative_to(basedir)).write_text(content)

    print("- Creating neutrapy config file ...")
    with (
        workdir.joinpath("neutralino.config.json").open() as f1,
        workdir.joinpath("pyproject.toml").open() as f2,
    ):
        neutrapy_config = {
            "name": args.name,
            "version": args.version,
            "description": args.description,
            "license": args.license,
            "neutralino": json.load(f1),
            "poetry": toml.load(f2),
        }
    with open(workdir.joinpath("neutrapy.toml"), "w") as f:
        toml.dump(neutrapy_config, f)

    print(f"- To run your application: cd {args.name} && neutrapy run")
