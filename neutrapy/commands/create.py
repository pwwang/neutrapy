import json
import shutil
from subprocess import Popen

import rtoml as toml
from pathlib import Path

from .. import current_platform_rs

TPL_DIR = Path(__file__).parent.parent.joinpath("templates")


def _read_default_neuconfig(template):
    with open(TPL_DIR.joinpath(template, "neutralino.config.json")) as f:
        return json.load(f)


def _read_default_pyproject(template):
    with open(TPL_DIR.joinpath(template, "pyproject.toml")) as f:
        return toml.load(f)


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

    print("- Creating neutrapy config file ...")
    neutrapy_config = {
        "name": args.name,
        "version": args.version,
        "description": args.description,
        "license": args.license,
        "neutralino": _read_default_neuconfig(args.template),
        "poetry": _read_default_pyproject(args.template),
    }
    with open(workdir.joinpath("neutrapy.toml"), "w") as f:
        toml.dump(neutrapy_config, f)

    print("- Writing neutralino config ...")
    with open(workdir.joinpath("neutralino.config.json"), "w") as f:
        neuconfig = neutrapy_config["neutralino"]
        neuconfig = replace_placeholders(
            neuconfig,
            name=args.name,
            version=args.version,
            description=args.description,
            license=args.license,
            target=target,
            python=Path(args.python).as_posix(),
        )

        json.dump(neuconfig, f, indent=4)

    print("- Writing pyproject.toml ...")
    with open(workdir.joinpath("pyproject.toml"), "w") as f:
        pyproject = neutrapy_config["poetry"]
        pyproject = replace_placeholders(
            pyproject,
            name=args.name,
            version=args.version,
            description=args.description,
            license=args.license,
            target=target,
            python=Path(args.python).as_posix(),
        )

        toml.dump(pyproject, f)

    print("- Creating python extension for neutralino ...")
    extdir = workdir.joinpath("extensions")
    extdir.mkdir()
    tpldir = TPL_DIR.joinpath(args.template)
    shutil.copytree(
        tpldir.joinpath("extension"),
        extdir.joinpath("python"),
    )

    neu_ext_utils = replace_placeholders(
        tpldir.joinpath("extension", "utils.py").read_text(),
        name=args.name,
        version=args.version,
        description=args.description,
        license=args.license,
        target=target,
        python=Path(args.python).as_posix(),
    )
    extdir.joinpath("python", "utils.py").write_text(neu_ext_utils)
    extdir.joinpath("__init__.py").touch()

    print("- Copying frontend files ...")
    shutil.copyfile(
        tpldir.joinpath("index.html"),
        workdir.joinpath("resources", "index.html"),
    )
    shutil.copyfile(
        tpldir.joinpath("styles.css"),
        workdir.joinpath("resources", "styles.css"),
    )
    mainjs = replace_placeholders(
        tpldir.joinpath("main.js").read_text(),
        name=args.name,
        version=args.version,
        description=args.description,
        license=args.license,
        target=target,
        python=Path(args.python).as_posix(),
    )
    workdir.joinpath("resources", "js", "main.js").write_text(mainjs)

    print(f"- To run your application: cd {args.name} && neutrapy run")
