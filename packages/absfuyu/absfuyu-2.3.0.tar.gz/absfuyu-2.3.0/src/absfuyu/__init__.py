"""
ABSFUYU
---
A small collection of code

LINKS
---
- Home page: https://pypi.org/project/absfuyu/
- Documentation: https://absolutewinter.github.io/absfuyu/

USAGE
---
`import absfuyu`
"""


# Module level
###########################################################################
__title__ = "absfuyu"
__author__ = "AbsoluteWinter"
__license__ = "MIT License"
__all__ = [
    # default
    "calculation", "util",
    # extra
    "sort", "fun",
    "pkg_data",
    "game", "tools", "extensions",
    # config
    "config",
    # Other
    "version",
    "everything",
]


# Library
###########################################################################
# default function
from .version import __version__
from .version import check_for_update


# default module
from . import calculation as cal
from . import util


# config
# from . import config as __config
# __config.welcome()
