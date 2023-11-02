"""
Absfuyu: Package data
---
Load package data

Version: 2.0.0
Date updated: 04/06/2023 (dd/mm/yyyy)

Feature:
- PkgData
"""


# Module level
###########################################################################
__all__ = [
    "DataList", "PkgData"
]


# Library
###########################################################################
from ast import literal_eval
from importlib.resources import read_binary
from pathlib import Path
from typing import Union
import zlib

from absfuyu.core import DATA_PATH
from absfuyu.logger import logger


# Legacy - depreciated soon
###########################################################################
def __data_validate(data_name: str) -> bool:
    """Validate if data exist"""
    DATA_LIST = [
        "dummy", "punishment_windows",
    ]
    if data_name not in DATA_LIST:
        return False
    else:
        return True

def __load_data_string(data_name: str):
    """Load data and convert into string"""
    data = read_binary("absfuyu.pkg_data", f"{data_name}.dat")
    decompressed_data = zlib.decompress(data).decode()
    return decompressed_data

def __data_string_to_list(data_string: str):
    """Convert data to list"""
    data = literal_eval(data_string)
    return data

def loadData(data_name: str):
    """Load data"""
    if __data_validate(data_name):
        return __data_string_to_list(__load_data_string(data_name))
    else:
        return None


# Class
###########################################################################
class DataList:
    DUMMY = None
    PWIN = None


class PkgData:
    """Package data maker/loader"""
    def __init__(self, data_name: str) -> None:
        self.name = data_name
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"
    def __repr__(self) -> str:
        return self.__str__()
    
    def _make_dat(self, data: str, name: Union[str, Path]):
        """
        data: string data
        name: name and location of the data
        """
        compressed_data = zlib.compress(str(data).encode(), zlib.Z_BEST_COMPRESSION)
        with open(name, "wb") as file:
            file.write(compressed_data)
    
    def load_dat_data(self, evaluate: bool = False):
        """
        Load `.dat` data from package resource
        
        evaluate: use `ast.literal_eval()` to evaluate string data
        """
        compressed_data = read_binary("absfuyu.pkg_data", self.name)
        data = zlib.decompress(compressed_data).decode()
        # return data
        return literal_eval(data) if evaluate else data

    def update_data(self, new_data: str):
        """Update existing data"""
        self._make_dat(data=new_data, name=DATA_PATH.joinpath(self.name))
        logger.debug("Data updated")


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)
