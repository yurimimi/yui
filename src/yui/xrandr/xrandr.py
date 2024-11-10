"""Xrandr calls."""
import os


def xrandr_set_brightness(value, display) -> None:
    """Calls xrandr with shell with args specified."""

    os.popen(f"xrandr --output {display} --brightness {value:.2f}")


def xrandr_get_brightness(display):
    """Get brightness level of specified display with xrandr."""

    res = os.popen("xrandr --verbose --current | grep "+display+" -A5 | tail -n1 | awk '{print $NF}'").read()[:-1]
    return float(res)


def get_list_of_monitors():
    """Get list of monitors currently being used."""

    res = os.popen("xrandr --listmonitors | awk '{print $4}'").read()
    list_of_monitors = list(i for i in res.split('\n') if i)

    return list_of_monitors
