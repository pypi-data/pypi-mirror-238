import argparse
import sys

from ._version import __version__


def main():
    parser = argparse.ArgumentParser(prog="apix")
    parser.add_argument("--version", action="version", version=__version__)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
