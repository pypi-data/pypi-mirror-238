"""
Helpers for colored output with the Rich package.
"""
from functools import lru_cache
from sys import exit
from typing import Any, Union

from rich.console import Console
from rich.panel import Panel
from rich.pretty import pprint
from rich.text import Text
from rich.theme import Theme

from trongrid_extractoor.helpers.color_picker import ColorPicker
from trongrid_extractoor.helpers.string_constants import CONTRACT_ADDRESS

### Printing ###
INDENT_SPACES = 4

BYTES = 'color(100) dim'
BYTES_NO_DIM = 'color(100)'
BYTES_BRIGHTEST = 'color(220)'
BYTES_BRIGHTER = 'orange1'
BYTES_HIGHLIGHT = 'color(136)'
DARK_GREY = 'color(236)'
GREY = 'color(239)'
GREY_ADDRESS = 'color(238)'
PEACH = 'color(215)'
PURPLE = 'color(20)'

COLOR_THEME_DICT = {
    # colors
    'dark_orange': 'color(58)',
    'grey': GREY,
    'grey.dark': DARK_GREY,
    'grey.dark_italic': f"{DARK_GREY} italic",
    'grey.darker_italic': 'color(8) dim italic',
    'grey.darkest': 'color(235) dim',
    'grey.light': 'color(248)',
    'off_white': 'color(245)',
    'purple_grey': "color(60) dim italic",
    # functions
    'function': 'cyan',
    'arg_type': 'color(240)',
    'arg_name': 'magenta',
    # bytes
    'ascii': 'color(58)',
    'ascii_unprintable': 'color(131)',
    'bytes': BYTES,
    'bytes.title_dim': 'orange1 dim',
    'bytes.title': BYTES_BRIGHTER,
    'bytes.decoded': BYTES_BRIGHTEST,
    # other
    'transaction_id': 'color(220) bold',
    CONTRACT_ADDRESS: 'color(150) bold',
    'contract_owner': 'color(189)',
    'time': 'color(21) bold',
}


console = Console(theme=Theme(COLOR_THEME_DICT), color_system='256')
color_picker = ColorPicker()


def print_error_and_exit(error_msg: str) -> None:
    txt = Text('').append('ERROR', style='bright_red').append(f": {error_msg}")
    console.print(txt)
    exit(1)


def print_section_header(msg: Union[str, Text]) -> None:
    msg = str(msg)
    console.print(Panel(msg, style='reverse', width=max(40, len(msg) + 4)))


def pretty_print(obj: Any) -> None:
    """Thin wrapper around rich.pretty.pprint()."""
    pprint(obj, expand_all=True, indent_guides=False)
