"""TUI functions"""
from typing import List
from survey import printers, routines, colors


def notify(message: str, msg_type: str="info") -> None:
    """Notify user that something happend."""

    if msg_type == "info":
        printers.info(message)
    elif msg_type in ("err", "error", "fail", "warn", "warning"):
        printers.fail(message, mark="x")
    elif msg_type in ("done", "ok"): # I can add something else here
        printers.done(message, mark="v")
    elif msg_type in ("still", "unchanged", "nochange", "none", "nothing"):
        printers.info(message, mark="o", mark_color=colors.basic(fg="yellow"))


def proceed(message: str, attempt_num=0) -> bool:
    """Asks user for confirmation.

    User given with 3 attempts to choose y(es) or n(o). Returns True or False respectively.
    """

    printers.info(message)

    # Give them 3 attempts
    if attempt_num == 3:
        return False

    answer = input("Proceed anyway? Y/n: ")
    result = None

    if answer in ("y", "Y", "yes", "Yes", "YES"):
        result = True
    elif answer in ("n", "N", "no", "No", "NO"):
        result = False

    if result is None:
        return proceed(attempt_num+1)

    return result


def ask_select(message: str, options: List[str]) -> int:
    """Asks the user to choose one of the options provided and returns the index
    on user has chosen"""

    return routines.select(message, options=options)


def ask_input(message: str) -> str:
    """Asks the user for input a text. Returns string of the input"""

    return routines.input(message)
