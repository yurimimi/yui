"""Check battery charge at the current time."""
import os
import logging
from ..ui import notify


logger = logging.getLogger(__name__)


# Add such thing to each script in the utils directory
YUM_HELP = """Check battery charge at the current time.

If no arguments provided shows sum of all batteries available.

Parameters
----------
battery_num : int, optional
    The battery to show charge of (default is None)"""


def battery_check(battery_num: int | None=None) -> None:
    """Check battery charge at the current time.

    If no arguments provided shows sum of all batteries available.

    Parameters
    ----------
    battery_num : int, optional
        The battery to show charge of (default is None)
    """

    if not isinstance(battery_num, int) and battery_num is not None:
        logger.warning("Please, choose a battery to check the charge of or just enter to get sum.")
        return

    power_supply_dir = "/sys/class/power_supply/"

    bat_dirs = [f for f in os.listdir(power_supply_dir) if              \
                os.path.isdir(os.path.join(power_supply_dir, f)) and
                f.startswith('BAT')]

    logger.debug("BAT dirs %s", bat_dirs)

    charges = []

    for bat in bat_dirs:
        logger.debug(bat)
        cap_file_abs_path = os.path.join(power_supply_dir, bat, "capacity")
        with open(cap_file_abs_path, "r", encoding="utf-8") as c:
            charge = int(c.read())
            charges.append(charge)

    logger.debug("charges of batts %s", charges)

    sum_of_charges = sum(charges) / 2.

    logger.debug("sum of charges %s%%", sum_of_charges)
    if battery_num is None:
        notify(f"{sum_of_charges}% ({len(charges)} batteries)")
    else:
        notify(f"Battery {battery_num} charge: {charges[battery_num]}%")


def main(args=None) -> None:

    if args is None or args == "":
        battery_check()
    else:
        try:
            battery_check(int(args))
        except ValueError:
            logger.warning("Argument is not an int number.")


if __name__ == "__main__":
    main()
