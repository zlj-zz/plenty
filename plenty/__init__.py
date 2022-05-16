from typing import TYPE_CHECKING, Optional
import os

# For windows print color.
if os.name == "nt":
    os.system("")


if TYPE_CHECKING:
    from .console import Console


_console: Optional["Console"] = None


def get_console():
    global _console

    if not _console:
        from .console import Console

        _console = Console()

    return _console


def echo(*values, sep: str = " ", end: str = "\n", file=None, flush: bool = True):
    value_list = [get_console().render_str(str(value)) for value in values]
    print(*value_list, sep=sep, end=end, file=file, flush=flush)
