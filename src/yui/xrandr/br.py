"""Xrandr calls"""
import subprocess
import shlex


def xrandr_set_brightness(value, display="eDP-1") -> None:
    """Calls xrandr with shell with args specified."""

    subprocess.call(shlex.split(f"xrandr --output {display} --brightness {value:.2f}"))


def xrandr_get_brightness(display="eDP-1"):
    """Get brightness level of specified display with xrandr."""

    with subprocess.Popen(shlex.split("xrandr --verbose --current"),
                          stdout=subprocess.PIPE) as p1:
        with subprocess.Popen(shlex.split(f"grep {display} -A5"),
                         stdin=p1.stdout, stdout=subprocess.PIPE) as p2:
            with subprocess.Popen(shlex.split("tail -n1"),
                                  stdin=p2.stdout, stdout=subprocess.PIPE) as p3:
                with subprocess.Popen(shlex.split("awk '{print $NF}'"),
                                      stdin=p3.stdout, stdout=subprocess.PIPE) as p4:
                    return p4.communicate()[0]
