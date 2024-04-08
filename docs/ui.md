UI module is an abstraction of the [survey](https://github.com/Exahilosys/survey) lib I
use for the menus of this app.

# UI module

functions

notify(message: str, msg_type: str="info") -> None

    Notify user that something happend.
    Accepts message string to display it on the user's shell. The second argument is a
    string denoting the type of message: for info "info"; for error "err", "error", "fail",
    "warn", "warning"; for done use "done" or "ok".

proceed(message: str) -> bool

    Asks user for confirmation.
    User given with 3 attempts to choose y(es) or n(o). Returns True or False respectively.

def ask_select(message: str, options: List[str]) -> int:

    Asks the user to choose one of the options provided and returns the index on user has
    chosen.

def ask_input(message: str) -> str:

    Asks the user for input a text. Returns string of the input or empty string on empty
    input.
