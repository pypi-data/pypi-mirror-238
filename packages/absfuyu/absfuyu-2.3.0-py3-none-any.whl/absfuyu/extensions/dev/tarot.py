"""
Absfuyu: Tarot
---
Tarot stuff

Version: 1.0.0
Date updated: 05/06/2023 (dd/mm/yyyy)
"""

# Module level
###########################################################################
__all__ = [
    "Tarot"
]


# Library
###########################################################################
import random
from typing import Dict, List

from absfuyu.core import DATA_PATH
from absfuyu.logger import logger
from absfuyu.util.api import APIRequest


# Class
###########################################################################
class TarotCard:
    """Tarot card"""
    def __init__(
            self,
            name: str,
            rank: int,
            suit: str,
            meanings: Dict[str, List[str]],
            keywords: List[str],
            fortune_telling: List[str]
        ) -> None:
        self.name = name.title()
        self.rank = rank
        self.suit = suit
        self.meanings = meanings
        self.keywords = keywords
        self.fortune_telling = fortune_telling
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"
    def __repr__(self) -> str:
        return self.__str__()


class Tarot:
    """Tarot data"""
    def __init__(self) -> None:
        self.data = APIRequest(
            "https://raw.githubusercontent.com/dariusk/corpora/master/data/divination/tarot_interpretations.json",
            encoding="utf-8"
        )
        self.data_location = DATA_PATH.joinpath("tarot.json")
    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"
    def __repr__(self) -> str:
        return self.__str__()

    def _load(self, update: bool = False) -> List[TarotCard]:
        """
        Load tarot json data from API

        update: refresh the cache
        """
        json_data = self.data.fetch_data(
            update=update,
            json_cache=self.data_location
        )
        tarot_data = json_data["tarot_interpretations"]
        logger.debug(f"{len(tarot_data)} tarot cards loaded")
        # return tarot_data
        return [
            TarotCard(
                name=x["name"],
                rank=x["rank"],
                suit=x["suit"],
                meanings=x["meanings"],
                keywords=x["keywords"],
                fortune_telling=x["fortune_telling"]
            ) for x in tarot_data
        ]
    
    def random_card(self):
        """Pick a random tarot card"""
        return random.choice(self._load())

# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)
    from rich import print
    test = Tarot()
    print(test.random_card())