"""
Absfuyu: Core
---
Contain type hint and other stuff

Version: 2.0.0
Date updated: 05/06/2023 (dd/mm/yyyy)
"""

# Module Package
###########################################################################
ModulePackage = [
    "all",
    "cli",
    "beautiful", "extra", "tools",
    "test", "dev", "fixers",
]
ModuleList = [
    "calculation",
    "sort", "util", "fun",
    "pkg_data", "config",
    "extensions", "game", "tools", "version"
]


# Library
###########################################################################
import os
from pathlib import Path
from typing import (
    Dict as __Dict,
    TypeVar as __TypeVar,
    Union as __Union,
)

from sys import version_info as __py_ver # Get python version
if __py_ver[0] == 3:
    # Python 3.7.x
    if __py_ver[1] == 7:
        try:
            from typing_extensions import Literal as __Literal
        except ImportError as err:
            # Auto install
            from subprocess import run as __run
            __cmd = [
                # "python -m pip install --upgrade pip".split(),
                "python -m pip install typing_extensions".split(),
            ]
            for x in __cmd:
                __run(x)
            # raise SystemExit(err)
    # Not python 3.7.x | Python >= 3.8
    else:
        from typing import Literal as __Literal
else:
    raise SystemExit("Not Python 3")

# Check for colorama library
try:
    import colorama as __colorama
except ImportError:
    __colorama = None




# Color - colorama
###########################################################################
if __colorama is not None:
    # __colorama.init(autoreset=True)
    Color: __Dict[str, str] = {
        "green": __colorama.Fore.LIGHTGREEN_EX,
        "GREEN": __colorama.Fore.GREEN,
        "blue": __colorama.Fore.LIGHTCYAN_EX,
        "BLUE": __colorama.Fore.CYAN,
        "red": __colorama.Fore.LIGHTRED_EX,
        "RED": __colorama.Fore.RED,
        "yellow": __colorama.Fore.LIGHTYELLOW_EX,
        "YELLOW": __colorama.Fore.YELLOW,
        "reset": __colorama.Fore.RESET
    }
else:
    Color = {
        "green": "",
        "GREEN": "",
        "blue": "",
        "BLUE":"",
        "red": "",
        "RED": "",
        "yellow": "",
        "YELLOW": "",
        "reset": ""
    }


# Type hints
###########################################################################
Number = __TypeVar("Number", int, float)
NumberC = __TypeVar("NumberC", int, float, complex)

# Random string generator
CharacterOption = __Literal[
    "default", "alphabet", "full", "uppercase",
    "lowercase", "digit", "special", "all"
]

# Other
MonthLong = __Literal["january", "february", "march", "april", "may", "june", "july", "august" , "september", "october", "november", "december"]
MonthShort = __Literal["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug" , "sep", "oct", "nov", "dec"]
Month = __Union[MonthShort, MonthLong]

#
Opt3 = __Union[__Literal[True], __Literal[False], None]
AlignPosition = __Literal["left", "right", "center"]


# Path
CORE_PATH = Path(os.path.abspath(os.path.dirname(__file__)))
CONFIG_PATH = CORE_PATH.joinpath("config", "config.json")
DATA_PATH = CORE_PATH.joinpath("pkg_data")