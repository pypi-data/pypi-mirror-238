# -*- coding: utf-8 -*-
"""
Absufyu: Json Method
---
json handling

Version: 1.0.0
Date updated: 27/05/2023 (dd/mm/yyyy)

Feature:
- JsonFile
"""


# Module level
###########################################################################
__all__ = [
    "JsonFile"
]


# Library
###########################################################################
import json
from pathlib import Path
from typing import Union

from absfuyu.logger import logger


# Function
###########################################################################
def load_json(json_file_location: str):
    """Load JSON file"""
    with open(json_file_location, "r") as json_file:
        data = json.load(json_file)
    return data


# Class
###########################################################################
class JsonFile:
    """
    json handling
    """
    def __init__(
            self,
            json_file_location: Union[str, Path],
            *,
            encoding: Union[str, None] = "utf-8",
            indent: Union[int, str, None] = 4,
            sort_keys: bool = True
        ) -> None:
        """
        json_file_location: json file location
        encoding: data encoding (default: utf-8)
        indent: indentation when export to json file
        sort_keys: sort the keys before export to json file
        """
        self.json_file_location = Path(json_file_location)
        self.encoding = encoding
        self.indent = indent
        self.sort_keys = sort_keys
        self.data = {}
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.json_file_location.name})"
    def __repr__(self) -> str:
        return self.__str__()
    
    def load_json(self) -> dict:
        """Load json file"""
        with open(self.json_file_location, "r", encoding=self.encoding) as file:
            self.data = json.load(file)
        return self.data

    def save_json(self):
        """Save json file"""
        json_data = json.dumps(self.data, indent=self.indent, sort_keys=self.sort_keys)
        with open(self.json_file_location, "w", encoding=self.encoding) as file:
            file.writelines(json_data)


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)