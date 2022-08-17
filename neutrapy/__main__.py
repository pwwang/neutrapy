import sys
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

    if len(sys.argv) > 1 and sys.argv[1] == "run" and "--" in sys.argv:
        main_args, sub_args = (
            sys.argv[1:sys.argv.index("--")],
            sys.argv[sys.argv.index("--") + 1:],
        )
        args = params.parse(main_args)
        args[args.__command__]["-"] = sub_args
    else:
        args = params.parse()

    try:
        module = import_module(f".commands.{args.__command__}", __package__)
    except ImportError:
        raise NotImplementedError(f"No such command `{args.__command__}`")

    module.run(args[args.__command__])

if __name__ == "__main__":
    main()
