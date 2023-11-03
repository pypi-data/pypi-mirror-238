import argparse
import sys

from pathier import Pathier
from younotyou import younotyou


def get_scripts_windows() -> list[str]:
    """Returns a list of script stems for any `.exe` file in the current Python interpreter's `Scripts` folder."""
    pypath = Pathier(sys.executable)
    return [file.stem for file in (pypath.parent / "Scripts").glob("*.exe")]


def get_scripts_unix() -> list[str]:
    """Returns a list of scripts from `~/.local/bin`."""
    return [file.name for file in (Pathier.home() / ".local" / "bin")]


def get_scripts() -> list[str]:
    """Returns a list of scripts."""
    if sys.platform == "win32":
        return get_scripts_windows()
    else:
        return get_scripts_unix()


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "includes",
        nargs="*",
        type=str,
        default=["*"],
        help=""" A list of wildcard patterns to search for scripts with.
        i.e. >scriptcheck a* d*
        will only print scripts starting with an 'a' or a 'd'.""",
    )
    args = parser.parse_args()

    return args


def main(args: argparse.Namespace | None = None):
    if not args:
        args = get_args()
    print(*[script for script in younotyou(get_scripts(), args.includes)], sep="\n")


if __name__ == "__main__":
    main(get_args())
