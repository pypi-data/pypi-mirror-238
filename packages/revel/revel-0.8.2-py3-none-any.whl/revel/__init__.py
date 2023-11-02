import colorama

from .cli_app import App, Parameter
from .legacy import *
from .markup import GLOBAL_STYLES, unescape
from .style import *

colorama.init()

__all__ = [
    "print",
    "print_chapter",
    "warning",
    "error",
    "fatal",
    "input",
    "ask",
    "ask_short",
    "ask_yes_no",
]
