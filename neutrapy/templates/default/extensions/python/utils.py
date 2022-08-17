import json
import logging
from pathlib import Path

import rtoml as toml


def runtime_info():
    infofile = Path.cwd().joinpath(".tmp", "auth_info.json")
    with open(infofile) as f:
        return json.load(f)


EXT_ID = "js.neutralino.${name}.python"
RUNTIME_INFO = runtime_info()
NEU_TOKEN = RUNTIME_INFO["accessToken"]
NEU_URL = (
    f"ws://127.0.0.1:{RUNTIME_INFO['port']}"
    "?extensionId=js.neutralino.${name}.python"
)


def get_logger():
    logger = logging.getLogger(EXT_ID)
    if logger.handlers:
        return logger

    with open(Path.cwd().joinpath("neutrapy.toml")) as f:
        config = toml.load(f)

    fh = logging.FileHandler(
        Path.cwd().joinpath(f"{EXT_ID}.log")
    )
    logger.addHandler(fh)
    logger.setLevel(config.get("ext-loglevel", "INFO"))
    return logger


LOGGER = get_logger()
