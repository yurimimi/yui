"""Display brightness level manager manipulating xrandr."""
import logging
from typing import TypeVar

from ..ui import proceed, notify # I have to decouple this
from ..xrandr import br


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


YUM_HELP = """Set display brightness.

You can set it in range between 0 to 100 by specifying an abs value (0-100) or by a 
relative value, for example -10 or +30. Uses xrandr. 

Parameters
----------
brt_level : int | str, optional
    Absolute or relative value of brightness"""


T = TypeVar("T")


def _pass_filter(val: T, min_pass: T, max_pass: T) -> T:
    try:
        return max(min_pass, min(val, max_pass))
    except ValueError as e:
        raise e


def set_brightness(brt_level: int | str=None) -> None:
    """Set display brightness level from 10 to 100. Uses xrandr."""

    # Flag that indicates either the value is relative (in percents) or absolute (from 0 to 100)
    brt_is_rel = False
    rel_sign: str | int # first str then int

    # If arg is None
    if brt_level is None:

        notify("Please set a value in range from 0 to 100.", msg_type="err")
        logger.warning("Please set a value in range from 0 to 100.")

        return

    # If arg is a string with a sign
    if brt_level.startswith("-") or brt_level.startswith("+"):
        rel_sign = int(brt_level[0] + "1")
        brt_level = int(brt_level[1:])
        logger.debug("Brightness level to set before calc: %s", brt_level)
        brt_is_rel = True
    else:
        try:
            brt_level = int(brt_level)
        except ValueError as e:
            print(e, "Please set a value in range from 0 to 100.")

    # Check if arg is in range between 0 and 100
    if brt_level in range(101):
        # Translate in range of 0 to 1
        brt_level /= 100

        # If arg was provided with a sign
        if brt_is_rel:

            # Calculate what brightness level we get here after application of the rel value
            curr_brt = float(br.xrandr_get_brightness())
            logger.debug("Current brightness: %s", curr_brt)

            # Calc. Here's the 0.8 - 0.1 = 0.7000000000000001 kind of problem so I do `round`
            val = round(curr_brt + rel_sign * brt_level, 2)

            # Restrict it to 0-1
            brt_level = _pass_filter(val, 0, 1)
            logger.debug("Brightness level to set after calc: %s", brt_level)

        # Notify user that the brightness to set is a very low value
        # Ask user if they want it
        if brt_level <= .05 and not proceed("You're trying to set value of <5"):
            # Exit
            return

        # Set brightness to specified value
        br.xrandr_set_brightness(brt_level)

        logger.info("Brightness level set to %s", brt_level)
        notify(f"Brightness level set to {brt_level}", msg_type="ok")

        return

    # If arg value is out of range of 0 to 100
    notify("Please set a value in range from 0 to 100.", msg_type="err")
    logger.warning("Please set a value in range from 0 to 100.")


def main(args=None) -> None:

    set_brightness(args)


if __name__ == "__main__":
    main()
