import os
import shutil
from functools import lru_cache
from contextlib import contextmanager
from pathlib import Path
from subprocess import check_output


def replace_placeholders(config: str, **values) -> str:

    for key, value in values.items():
        config = config.replace(f"${{{key}}}", str(value))

    return config


def logh(h):
    """Log a message as a heading"""
    print()
    print(h)
    print("-" * len(h))


@lru_cache()
def get_python_version(python, parts=3):
    """Get the version of the given python executable"""
    if parts == 3:
        return check_output(
            [
                python,
                "-c",
                "import sys; print('.'.join(map(str, sys.version_info[:3])))",
            ],
            encoding="utf-8",
        )

    if parts == 2:
        return ".".join(get_python_version(python).split(".")[:2])

    return get_python_version(python).split(".")[0]


@contextmanager
def set_dir(path):
    """Set the current working directory"""
    origin = Path().cwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)


@contextmanager
def backingup(file):
    """Backup a file before modifying it and finally restore it"""
    backup = file.parent.joinpath(f"{file.name}.bak")
    shutil.copyfile(file, backup)

    try:
        yield
    finally:
        shutil.move(backup, file)
