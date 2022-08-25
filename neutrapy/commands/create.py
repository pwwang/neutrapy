import json
import shutil
from pathlib import Path
from subprocess import Popen

import rtoml as toml
from slugify import slugify

from ..current_platform_rs import platform
from ..utils import logh, replace_placeholders, set_dir, get_python_version
from .sync import run as run_sync

TPL_DIR = Path(__file__).parent.parent.joinpath("templates")


def run(args):
    """Create a new project"""
    workdir = Path.cwd().joinpath(args.name)
    if workdir.exists() and not args.force:
        raise FileExistsError(
            f"Directory `{workdir}` already exists, "
            "try --force to overwrite it."
        )

    if workdir.is_dir():
        logh("Removing existing project directory")
        shutil.rmtree(workdir)

    logh("Creating neutralinojs project")
    Popen([shutil.which("neu"), "create", args.name]).wait()

    logh("Copying template files")
    basedir = TPL_DIR.joinpath("default")
    tpldir = TPL_DIR.joinpath(args.template)
    python = shutil.which(args.python)
    data = dict(
        name=args.name,
        slug_name=slugify(args.name, separator="."),
        version=args.version,
        description=args.description,
        license=args.license,
        target=platform(),
        python=python,
        python_version=get_python_version(python),
        python_minor_version=get_python_version(python, parts=2),
        **{"ext-loglevel": args["ext-loglevel"]},
    )

    tplconffile = tpldir.joinpath(".neutrapy_template.toml")
    if tplconffile.is_file():
        with tplconffile.open() as f:
            tplconfig = toml.load(f)
    else:
        tplconfig = {}
    tplconfig.setdefault("excludes", [])
    tplconfig.setdefault("neujs_copy_to", False)
    tplconfig["excludes"].append(tplconffile.name)
    excludes = set((Path(exc) for exc in tplconfig["excludes"]))

    union_names = set(
        [name.relative_to(basedir) for name in basedir.glob("**/*")]
    ) | set(
        [name.relative_to(tpldir) for name in tpldir.glob("**/*")]
    )
    union_names = set(
        (
            uname
            for uname in union_names
            if uname not in excludes and not (excludes & set(uname.parents))
        )
    )

    # sort to make sure directories come first
    for uname in sorted(union_names):
        tfile = tpldir.joinpath(uname)
        if not tfile.exists():
            tfile = basedir.joinpath(uname)

        if tfile.is_dir():
            workdir.joinpath(uname).mkdir(parents=True, exist_ok=True)
            continue

        try:
            content = tfile.read_text()
        except UnicodeDecodeError:
            shutil.copyfile(tfile, workdir.joinpath(uname))
        else:
            if tfile.suffix == ".json":
                content = replace_placeholders(
                    content,
                    # escape the python path on windows
                    python=python.replace("\\", "\\\\"),
                    **{k: v for k, v in data.items() if k != "python"},
                )
            else:
                content = replace_placeholders(content, **data)

            workdir.joinpath(uname).write_text(content)

    if tplconfig["neujs_copy_to"]:
        shutil.copyfile(
            workdir.joinpath("resources", "js", "neutralino.js"),
            workdir.joinpath(tplconfig["neujs_copy_to"], "neutralino.js"),
        )

    for exc in tplconfig["excludes"]:
        excfile = workdir.joinpath(exc)
        if excfile.is_dir():
            shutil.rmtree(excfile)
        elif excfile.is_file():
            excfile.unlink()

    logh("Creating neutrapy config file")
    nconfigfile = tpldir.joinpath("neutralino.config.json")
    if not nconfigfile.exists():
        nconfigfile = basedir.joinpath("neutralino.config.json")
    pconfigfile = tpldir.joinpath("pyproject.toml")
    if not pconfigfile.exists():
        pconfigfile = basedir.joinpath("pyproject.toml")

    with nconfigfile.open() as f1, pconfigfile.open() as f2:
        neutrapy_config = {
            key: val
            for key, val in data.items()
            if key not in ("python_version", "python_minor_version")
        }
        neutrapy_config["neutralino"] = json.load(f1)
        neutrapy_config["poetry"] = toml.load(f2)

    with open(workdir.joinpath("neutrapy.toml"), "w") as f:
        toml.dump(neutrapy_config, f)

    with set_dir(workdir):
        run_sync(
            {},
            sync_pypj=False,
            sync_neu=False,
        )

    # So that we don't need to run `neu sync`
    workdir.joinpath("pyproject.toml").touch()
    workdir.joinpath("neutralino.config.json").touch()

    if workdir.joinpath("package.json").is_file():
        logh(
            f"To run your application: cd {args.name} && npm install && "
            "npm run build && neutrapy run"
        )
    else:
        logh(f"To run your application: cd {args.name} && neutrapy run")
