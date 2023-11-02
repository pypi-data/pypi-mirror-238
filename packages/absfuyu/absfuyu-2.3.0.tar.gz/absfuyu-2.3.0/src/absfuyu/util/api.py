# -*- coding: utf-8 -*-
"""
Absufyu: API
---
Fetch data stuff

Version: 1.0.0
Date updated: 26/05/2023 (dd/mm/yyyy)

Feature:
- APIRequest
"""


# Module level
###########################################################################
__all__ = [
    "APIRequest"
]


# Library
###########################################################################
import json
from pathlib import Path
from typing import Union

try:
    import requests
except ImportError as e:
    raise SystemExit(e)

from absfuyu.logger import logger


# Class
###########################################################################
class APIRequest:
    """API data with cache feature"""
    def __init__(
            self,
            api_url: str,
            *, # Use "*" to force using keyword in function parameter | Example: APIRequest(url, encoding="utf-8")
            encoding: Union[str, None] = "utf-8"
        ) -> None:
        """
        api_url: api link
        encoding: data encoding (default: utf-8)
        """
        self.url = api_url
        self.encoding = encoding
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.url})"
    def __repr__(self) -> str:
        return self.__str__()

    def fetch_data(
            self,
            *,
            update: bool = False,
            json_cache: Union[str, Path]
        ):
        """
        Fetch data from an API then cache it for later use

        update: Refresh the cache when `True`
        json_cache: Name of the cache
        """
        if update:
            json_data=None
        else:
            try:
                with open(json_cache, "r", encoding=self.encoding) as file:
                    json_data = json.load(file)
                    logger.debug("Fetched data from local cache!")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logger.debug(f"No local cache found... ({e})")
                json_data = None
        
        if not json_data:
            logger.debug("Fetching new json data... (Creating local cache)")
            try:
                json_data = requests.get(self.url).json()
                with open(json_cache, "w", encoding=self.encoding) as file:
                    json.dump(json_data, file, indent=2)
            except FileNotFoundError as e:
                logger.error(f"Can't create cache due to Path error - {e}")

        return json_data
    
    def fetch_data_only(self):
        """Fetch data without cache"""
        return requests.get(self.url)


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)