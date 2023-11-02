"""
Absufyu: Converter
---
Convert stuff

Version: 1.0.0
Date updated: 27/05/2023 (dd/mm/yyyy)

Feature:
- Text2Chemistry
"""


# Module level
###########################################################################
__all__ = [
    "Text2Chemistry"
]


# Library
###########################################################################
from itertools import combinations, chain
import math
import re
import string
from typing import List

from absfuyu.core import DATA_PATH
from absfuyu.logger import logger
from absfuyu.util.api import APIRequest


# Class
###########################################################################
class ChemistryElement:
    """Chemistry Element"""
    def __init__(
            self,
            name: str,
            number: int,
            symbol: str,
            atomic_mass: float
        ) -> None:
        """
        name: element name
        number: order in periodic table
        symbol: short symbol of element
        atomic_mass: atomic mass of element
        """
        self.name = name
        self.number = number
        self.symbol = symbol
        self.atomic_mass = atomic_mass
    def __str__(self) -> str:
        return self.symbol
    def __repr__(self) -> str:
        # return self.symbol
        return f"{self.__class__.__name__}({self.symbol})"

class Text2Chemistry:
    def __init__(self) -> None:
        self.data = APIRequest(
            "https://raw.githubusercontent.com/Bowserinator/Periodic-Table-JSON/master/PeriodicTableJSON.json",
            encoding="utf-8"
        )
        self.data_location = DATA_PATH.joinpath("chemistry.json")
    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"
    def __repr__(self) -> str:
        return self.__str__()
    
    def _load_chemistry_data(self, update: bool = False) -> List[ChemistryElement]:
        """
        Load chemistry json data from API

        update: refresh the cache
        """
        json_data = self.data.fetch_data(
            update=update,
            json_cache=self.data_location
        )
        elements = json_data["elements"]
        logger.debug(f"{len(elements)} elements loaded")
        return [
            ChemistryElement(
                name=element["name"],
                number=int(element["number"]),
                symbol=element["symbol"],
                atomic_mass=float(element["atomic_mass"])
            ) for element in elements
        ]
        
    @property
    def unvailable_characters(self):
        """
        Characters that can not be converted (unvailable chemistry symbol)
        """
        base = set(string.ascii_lowercase)
        available = set("".join(map(lambda x: x.symbol.lower(), self._load_chemistry_data())))
        # logger.debug(base)
        # logger.debug(available)
        return base.difference(available)
    
    def convert(self, text: str) -> List[List[ChemistryElement]]:
        """
        Convert text to chemistry symbol

        text: desired text

        returns: list (empty list when failed to convert)
        """
        # Check if `text` is a word (without digits)
        is_word_pattern = r"^[a-zA-Z]+$"
        if re.search(is_word_pattern, text) is None:
            logger.error("Convert Failed. Word Only!")
            raise ValueError("Convert Failed. Word Only!")
        for x in self.unvailable_characters:
            if text.find(x) != -1:
                logger.debug(f"{text} contains unvailable characters: {self.unvailable_characters}")
                # raise ValueError(f"Text contains {self.unvailable_character}")
                return []
        
        # Setup
        text_lower = text.lower()
        data = self._load_chemistry_data()
        
        # List possible elements
        possible_elements: List[ChemistryElement] = []
        for i, letter in enumerate(text_lower):
            for element in data:
                if element.symbol.lower().startswith(letter): # Check for `element.symbol` starts with `letter`
                    # logger.debug(f"{letter} {element}")
                    if element.symbol.lower().startswith(text_lower[i:i+len(element.symbol)]): # Check for `element.symbol` with len > 1 starts with `letter` of len(element.symbol)
                        possible_elements.append(element)
                    # Break when reach last letter in text
                    if letter == text_lower[-1]:
                        break
        logger.debug(possible_elements)
        if len(possible_elements) < 1: # No possible elements
            return []

        # temp = []
        # for i in range(min_combination_range, len(text_lower)+1):
        #     comb = combinations(possible_elements, i)
        #     temp.append(comb)
        # possible_combinations = chain(*temp)
        max_symbol_len = max(map(lambda x: len(x.symbol), possible_elements)) # Max len of `element.symbol`
        min_combination_range = math.ceil(len(text_lower) / max_symbol_len)
        logger.debug(f"Combination range: [{min_combination_range}, {len(text_lower)}]")
        possible_combinations = chain(*(combinations(possible_elements, i) for i in range(min_combination_range, len(text_lower)+1)))
        # logger.debug(list(possible_combinations))
        
        output = []
        for comb in possible_combinations:
            merged = "".join(map(lambda x: x.symbol, comb))
            if text_lower == merged.lower():
                output.append(list(comb))
                logger.debug(f"Found: {merged}")

        return output


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)