from cookiecutter.cli import main as ccmain
import sys
from pathlib import Path


def main():
    path = Path(__file__).absolute().parent.parent.joinpath('template').as_posix()
    sys.argv.append(path)
    ccmain()


if __name__ == "__main__":  # pragma: no cover
    main()
    