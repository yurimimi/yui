"""Normalize filenames in directory"""
import argparse
import logging
from filemanagement.core import Directory

from ..ui import notify


logger = logging.getLogger(__name__)


YUI_HELP = """Normalize filenames in directory

If no arguments provided normalizes all files in the current directory.

Parameters
----------
location : str, optional
    With -l or --location flag
    Absolute or relative path to the directory where normalizes filenames in.

force_rewrite : bool, optional
    With -f or --force flag
    Rewrites existing files if set to True. False by default."""


def main(args=None) -> None:

    # Set up args parser
    parser = argparse.ArgumentParser(
                        prog="Normalize filenames",
                        description="""This script removes some 'bad'
                        symbols from files' names in specified or
                        current directory (just spaces for now -3-)""",)
    parser.add_argument("-v", "--verbose",
                        help="""display information about all files
                        being processed""",
                        action="store_true",
                        required=False)
    parser.add_argument("-f", "--force",
                        help="""rewrite existing files if there are
                        name collisions""",
                        action="store_true",
                        required=False)
    parser.add_argument("-l", "--location",
                        help="""normalize files in this direction
                        (optional; only relative path)""",
                        type=str,
                        default='.')
    # Get all specified arguments
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args.split())

    directory = Directory(args.location)
    change_log = directory.normalize_filenames(force_rewrite=args.force)

    for log in change_log:
        name, new_name = log["names"]

        if log["status"] == "changed":
            notify(f"{name} -> {new_name}", "done")
        elif log["status"] == "collision":
            notify(f"{name} -> {new_name} already exists", "err")
        else:
            notify(f"{name}", "nochange")


if __name__ == "__main__":
    main()
