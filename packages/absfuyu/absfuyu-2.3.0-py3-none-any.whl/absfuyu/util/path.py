# -*- coding: utf-8 -*-
"""
Absfuyu: Path
---
Path related

Version: 1.2.0
Date updated: 17/08/2023 (dd/mm/yyyy)

Feature:
- DirStructure
- SaveFileAs
"""


# Module level
###########################################################################
__all__ = [
    "here_location", "location_wrap", "get_all_file_path",
    "DirStructure",
    "SaveFileAs"
]


# Library
###########################################################################
import os
from pathlib import Path
import re
from typing import Any, List, Union

from absfuyu.logger import logger


# Function
###########################################################################
def here_location():
    """
    Return current file location
    
    If fail then return current working directory
    """
    try:
        return os.path.abspath(os.path.dirname(__file__))
    except:
        return os.getcwd()
    
    # return os.path.abspath(os.path.dirname(__file__))

def location_wrap(file_location: str):
    """
    This function fix some `current working directory` error and return `abspath`
    """
    assert isinstance(file_location, str), "Must be a string"
    try: 
        here = here_location()
    except:
        here = ""
    return os.path.join(here, file_location)

def get_all_file_path(folder: str, *file_type: str):
    """
    Return a list of tuple: (path to choosen file type, filename)
    
    - `folder`: Folder path to search in
    - `file_type`: File type/extension without the "." symbol. 
    Support multiple file type (separate with "," (coma))
    (Example: `jpg`, `png`, `npy`)
    """
    # Check file type
    # If no `file_type` entered then proceed to print available file type
    if len(file_type) < 1:
        available_file_type = []
        for _, _, files in os.walk(folder):
            for file in files:
                temp = re.search(r"\b.*[.](\w+$)\b", file)
                if temp is not None:
                    available_file_type.append(temp[1])
        # print(f"Available file type: {set(available_file_type)}")
        # return list(set(available_file_type))
        # return None
        raise ValueError(f"Available file type: {set(available_file_type)}")

    # Generate regex pattern
    temp_pattern = "|".join(f"[.]{x}" for x in file_type)
    pattern = f"\\b^([\w ]+)({temp_pattern}$)\\b"
    # print("Search pattern: ", pattern)
    
    # Iter through each folder to find file
    file_location = []
    # for root, dirs, files in os.walk(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            result = re.search(pattern, file)
            if result is not None:
                file_location.append((os.path.join(root, file), result[1]))
    return file_location

def here_sniplet():
    """Return current file location code"""
    snip = """\
import os
here = os.path.abspath(os.path.dirname(__file__))

from pathlib import Path
here = Path(__file__)
"""
    return snip


# Class
###########################################################################
class DirStructure:
    def __init__(
            self,
            source_path: Union[str, Path],
            tab_symbol: str = "\t",
            sub_dir_symbol: str = "|-- "
        ) -> None:
        """
        source_path: Source folder to list folder structure
        tab_symbol: tab symbol
        sub_dir_symbol: subdirectory symbol
        """
        self.source_path = Path(source_path)
        self.tab_symbol = tab_symbol
        self.sub_dir_symbol = sub_dir_symbol
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.source_path})"
    def __repr__(self) -> str:
        return self.__str__()

    def _list_dir(self, *ignore: str):
        """List all directories and files"""
        logger.debug(f"Base folder: {self.source_path.name}")

        temp = self.source_path.glob("**/*")
        # No ignore rules
        if len(ignore) == 0:
            return (x.relative_to(self.source_path) for x in temp)

        # With ignore rules
        ignore_pattern = "|".join(ignore)
        logger.debug(f"Ignore pattern: {ignore_pattern}")
        return [x.relative_to(self.source_path) for x in temp if re.search(ignore_pattern, x.name) is None]

    def _separate_dir_and_files(self, list_of_path: List[Path]) -> List[str]:
        """Separate dir and file and transform into folder structure"""
        temp = sorted([str(x).split("/") for x in list_of_path]) # Linux
        if max(map(len, temp)) == 1:
            temp = sorted([str(x).split("\\") for x in list_of_path]) # Windows

        return [f"{self.tab_symbol*(len(x)-1)}{self.sub_dir_symbol}{x[-1]}" for x in temp]

    def list_structure(self, *ignore: str) -> str:
        """
        List folder structure

        Example
        ---
        For typical python library
        ```
        >>> test = DirStructure(<source path>)
        >>> test.list_structure(
                "__pycache__",
                ".pyc",
                "__init__", 
                "__main__",
                "tempCodeRunnerFile.py"
            )
        ...
        ```
        """
        temp = self._list_dir(*ignore)
        out = self._separate_dir_and_files(temp)
        return "\n".join(out)


class SaveFileAs:
    """File as multiple file type"""
    def __init__(
            self,
            data: Any,
            *,
            encoding: Union[str, None] = "utf-8"
        ) -> None:
        """
        :param encoding: Default: utf-8
        """
        self.data = data
        self.encoding = encoding
    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"
    def __repr__(self) -> str:
        return self.__str__()

    def to_txt(self, path: Union[str, Path]) -> None:
        """
        Save as .txt file
        
        :param path: Save location
        """
        with open(path, "w", encoding=self.encoding) as file:
            file.writelines(self.data)
    
    # def to_pickle(self, path: Union[str, Path]) -> None:
    #     """
    #     Save as .pickle file
        
    #     :param path: Save location
    #     """
    #     from absfuyu.util.pkl import Pickler
    #     Pickler.save(path, self.data)

    # def to_json(self, path: Union[str, Path]) -> None:
    #     """
    #     Save as .json file
        
    #     :param path: Save location
    #     """
    #     from absfuyu.util.json_method import JsonFile
    #     temp = JsonFile(path, sort_keys=False)
    #     temp.save_json()


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)
