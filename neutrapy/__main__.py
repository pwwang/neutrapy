from pathlib import Path
from importlib import import_module
from pyparam import Params


def main():
    params = Params(
        "neutrapy",
        desc="Command line tool for build a desktop app using "
        "neutralinojs and python"
    )
    params.from_file(Path(__file__).parent.joinpath("args.toml"))
    args = params.parse()

    try:
        module = import_module(f".commands.{args.__command__}", __package__)
    except ImportError:
        raise NotImplementedError(f"No such command `{args.__command__}`")

    module.run(args[args.__command__])

if __name__ == "__main__":
    main()
