from cookiecutter.cli import main as ccmain
import os, sys


def main():
    path = os.path.abspath(".") + "/template"
    print(path)
    sys.argv.append(path)
    ccmain()


if __name__ == "__main__":  # pragma: no cover
    main()
    