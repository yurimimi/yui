"""Set the new wallpaper picture for feh."""
import os
import sys

from ..ui import notify, proceed
from ..util import resolve_envvars


YUI_HELP = """Set the new wallpaper picture for feh.

Replaces the feh command in the .xinitrc file with a new one which specifies a 
new wallpaper's file path.

Parameters
----------
wallpaper_image_path : str
    Absolute path to picture file, accepting shell variables like $HOME."""


def set_wallpaper(wallpaper_image_path: str) -> None:
    wallpaper_image_path = resolve_envvars(wallpaper_image_path)
    config_file = ".xinitrc"
    config_file_path = os.path.join(os.getenv("HOME"), config_file)

    if not os.path.isfile(config_file_path):
        raise FileNotFoundError(f"File {config_file_path} doesn't exist.")

    #try:
    #    wallpaper_image_path = argv[1]
    #except:
    #    notify("Please, specify path to the wallpaper.")
    #    return 0

    if not os.path.isfile(wallpaper_image_path):
        notify(f"File '{wallpaper_image_path}' does not exist.")
        return 0

    # `.xinitrc` file lines
    config_file_lines: [str]
    # Line with which we replace the old one
    new_command = "feh --no-fehbg --bg-fill " + repr(wallpaper_image_path)

    # Update config: replace feh command with a new one with new wallpaper
    with open(config_file_path, 'r', encoding="utf-8") as config:
        config_file_lines = config.readlines()
    for line_num, line in enumerate(config_file_lines):
        if line.startswith("feh ") and "--bg-" in line:
            config_file_lines[line_num] = new_command + " &\n"

    # Check if the `feh ... --bg-...` command appears more than once.
    count = 0
    for line_num, line in enumerate(config_file_lines):
        if count < 2:
            if line.startswith("feh ") and "--bg-" in line:
                count += 1
        else:
            raise Exception("File contains more than one 'feh --bg-*' commands.")

    with open(config_file_path, 'w', encoding="utf-8") as config:
        config.writelines(config_file_lines)

    os.popen(new_command)

    notify(f"Set '{wallpaper_image_path}' as wallpapers.")


def main(args=None) -> None:
    set_wallpaper(args)


if __name__ == "__main__":
    #sys.exit(main(sys.argv))
    main()
