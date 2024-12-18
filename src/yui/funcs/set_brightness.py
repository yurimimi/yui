"""Screen brightness level manager, manipulating xrandr."""
import logging
from typing import TypeVar

from ..ui import ask_select, notify, proceed
from ..xrandr import xrandr


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


YUI_HELP = """Set display brightness.

You can set it in range between 0 to 100 by specifying an abs value (0-100) or by a 
relative value, for example -10 or +30. Uses xrandr. 

Parameters
----------
brt_level : int | str
    Absolute or relative value of brightness"""


T = TypeVar("T")


def _pass_filter(val: T, min_pass: T, max_pass: T) -> T:
    try:
        return max(min_pass, min(val, max_pass))
    except ValueError as e:
        raise e


def ask_monitor() -> str | list[str]:
    """"""

    # Will it be a problem with relative setting?
    list_of_monitors = xrandr.get_list_of_monitors()
    if not list_of_monitors:
        notify(msg_type="err", message="No monitors.")
        return
    # If there's only one option (single monitor) then just pass the iface down.
    elif len(list_of_monitors) == 1:
        return list_of_monitors[0]

    # Add an option to change for every monitor.
    list_of_monitors.append("Set to all")

    # Ask the user.
    message = "Please select a monitor to change the brightness of. "
    display_index = ask_select(message, list_of_monitors)
    display = list_of_monitors[display_index] 

    # Fix the mess.
    list_of_monitors = list_of_monitors[:-1]

    if display is "Set to all":
        notify(f"Setting to all monitors: {list_of_monitors} ")
        return list_of_monitors
    else:
        return display


def set_brightness(brt_level: int | str=None) -> None:
    """Set display brightness level from 10 to 100. Uses xrandr."""

    # Flag that indicates either the value is relative (+ or - to the current
    # value) or absolute (from 0 to 100).
    brt_is_rel: bool = False
    rel_sign: str | int | None = None

    # VALIDATION
    # If arg was not provided.
    if brt_level is None:
        notify("Please set a value in range from 0 to 100.", msg_type="err")
        # TODO This message should be more informative I guess.
        logger.warning("Please set a value in range from 0 to 100.") 
        # Exit this func since the value is invalid.
        return

    # If the argument is a string with a sign then format it as a relative value.
    if brt_level.startswith("-") or brt_level.startswith("+"):
        rel_sign = int(brt_level[0] + "1")
        brt_level = int(brt_level[1:])
        logger.debug("Brightness level to set before calc: %s", brt_level)
        brt_is_rel = True
    # Otherwise it's an absolute value, save it as is, or catch the exception 
    # on invalid value.
    else:
        try:
            brt_level = int(brt_level)
        except ValueError as e:
            print(e, "Please set a value in range from 0 to 100.")

    # Check if arg is into range between 0 and 100.
    # If the value is out of range of 0 to 100 warn the user and exit.
    if brt_level not in range(101):
        notify("Please set a value in range from 0 to 100.", msg_type="err")
        logger.warning("Please set a value in range from 0 to 100.")
        return
    # VALIDATION END

    # Which monitor or monitors to config.
    display: str | list[str] = ask_monitor()

    # Transform into range of 0 to 1.
    brt_level /= 100

    if isinstance(display, str):
        _set_brightness(display, brt_level, brt_is_rel, rel_sign)
    elif isinstance(display, list):
        for d in display:
            _set_brightness(d, brt_level, brt_is_rel, rel_sign)
    else:
        logger.warn("Invalid value. But how?")
        return 


def _set_brightness(display, brt_level, brt_is_rel=False, rel_sign=None):
    """Set display brightness level from 10 to 100. Uses xrandr.
    Finally.
    """

    # If value was provided with a sign
    if brt_is_rel:
        # Calculate what brightness level we get here after application of the 
        # rel value.
        curr_brt = float(xrandr.xrandr_get_brightness(display))
        logger.debug("Current brightness: %s", curr_brt)

        # Calc and also here's the 0.8 - 0.1 = 0.7000000000000001 kind of 
        # problem so I `round` the result.
        val = round(curr_brt + rel_sign * brt_level, 2)

        # Filter it into 0-1
        brt_level = _pass_filter(val, 0, 1)
        logger.debug("Brightness level to set after calc: %s", brt_level)

    # Notify user that the brightness to set is a very low value.
    # Ask the user if they want to anyway.
    if brt_level <= .05 and not proceed("You're trying to set value of <5"):
        # Exit
        return

    # Set brightness to the specified value.
    xrandr.xrandr_set_brightness(brt_level, display)

    logger.info("Brightness level set to %s", brt_level)
    notify(f"Brightness level set to {brt_level} for {display}.", msg_type="ok")


def main(args=None) -> None:
    set_brightness(args)


if __name__ == "__main__":
    main()
