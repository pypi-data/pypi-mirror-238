"""
Absfuyu: Config [W.I.P]
---
Package versioning module

Version: 2.0.0
Date updated: 22/05/2023 (dd/mm/yyyy)

Features:
- Config
"""


# Module level
###########################################################################
__all__ = [
    "Config",
]


# Library
###########################################################################
from dataclasses import dataclass
import json
from pathlib import Path

from absfuyu.core import CONFIG_PATH
from absfuyu.logger import logger
from absfuyu.util.json_method import load_json


# Class
###########################################################################
class Config:
    """
    Config handling
    """
    def __init__(self, config_file: Path, name: str = "config") -> None:
        self.config_path = config_file
        self.data = load_json(self.config_path)
        self.name = name
    def __str__(self) -> str:
        return ""
    def __repr__(self) -> str:
        return self.__str__()

    def save_to_json(self):
        """Save config"""
        cfg = json.dumps(self.data, indent=4, sort_keys=True)
        with open(self.config_path, "w", encoding="utf-8") as json_cfg:
            json_cfg.writelines(cfg)
        return None


# Init
###########################################################################
config = Config(CONFIG_PATH)


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)
    config = Config(CONFIG_PATH)