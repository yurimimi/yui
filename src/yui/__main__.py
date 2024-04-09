"""A CLI tool that catalogues utilities.

Yum is a utility manager that provides the user with a CLI menu with various utilities,
from image editors to file management systems. You are very welcome to fork it and
modify so that it becomes your utility manager!
"""
import sys
import os
import logging
import importlib
import signal
#import shutil

from .ui import notify, ask_select, ask_input


LOG_FORMAT = '%(asctime)s:%(levelname)s:%(name)s:%(lineno)d:%(message)s'
LOG_FORMAT_DATE = '%Y-%m-%d %I:%M:%S %p'


def _init():
    user_home_dir = os.path.expanduser("~")
    #user_config_dir = os.path.join(user_home_dir, ".config/yui")
    #user_config = os.path.join(user_config_dir, "config.py")
    user_share_dir = os.path.join(user_home_dir, ".local/share/yui")
    log_file = os.path.join(user_share_dir, "yui.log")

    if not os.path.isfile(log_file):
        os.makedirs(user_share_dir, exist_ok=True)

    #if not os.path.isfile(user_config):
    #    os.makedirs(user_config_dir, exist_ok=True)
        #shutil.copyfile("config.py", user_config) # copying not from the root dir

    #logger = logging.getLogger(__name__)
    logging.basicConfig(filename=log_file,
                        encoding="utf-8",
                        level=logging.DEBUG,
                        format=LOG_FORMAT,
                        datefmt=LOG_FORMAT_DATE)


def main() -> None:
    _init()

    main_dir = os.path.dirname(os.path.realpath(__file__))

    funcs_dir_name = "funcs"
    funcs_dir = os.path.join(main_dir, funcs_dir_name)

    funcs_list = [func[:-3] for func in os.listdir(funcs_dir)
                  if func.endswith(".py") and not func.startswith("_")]

    notify('Press Ctrl+C to quit.')
    # Ask user what function to use
    index = ask_select("Pick a function: ", options=funcs_list)
    # Get function name
    chosen_func = funcs_list[index]
    # Dynamically load the module
    func_module = importlib.import_module("." + funcs_dir_name + "." + chosen_func,
                                          package="yui")
    # Pring YUI_HELP of chosen script
    notify(func_module.YUI_HELP)

    # Ask user to provide arguments for the function
    args = ask_input('args: ')

    # Call function with arguments specified
    func_module.main(args)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt as e:
        print('\n')
        notify("Exiting...")
        sys.exit(0)
