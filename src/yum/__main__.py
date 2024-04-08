"""A CLI tool that catalogues all my python scripts and utilities"""

import sys
import os
import logging
import importlib

from .ui import notify, ask_select, ask_input


logger = logging.getLogger(__name__)
logging.basicConfig(filename="main.log", encoding="utf-8",
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p')


def main() -> None:

    main_dir = os.path.dirname(os.path.realpath(__file__))

    funcs_dir_name = "funcs"
    funcs_dir = os.path.join(main_dir, funcs_dir_name)

    funcs_list = [func[:-3] for func in os.listdir(funcs_dir)
                  if func.endswith(".py") and not func.startswith("_")]

    # Ask user what function to use
    index = ask_select("Pick a function: ", options=funcs_list)
    # Get function name
    chosen_func = funcs_list[index]
    # Dynamically load the module
    func_module = importlib.import_module("." + funcs_dir_name + "." + chosen_func,
                                          package="yum")
    # Pring yum_help of chosen script
    notify(func_module.YUM_HELP)

    # Ask user to provide arguments for the function
    args = ask_input('args: ')
    # Call function with arguments specified
    func_module.main(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
