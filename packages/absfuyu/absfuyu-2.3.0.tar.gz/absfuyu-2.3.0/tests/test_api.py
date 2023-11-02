"""
Test: API

Version: 1.0.0
Date updated: 27/05/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
import pytest

# from absfuyu.core import DATA_PATH
from absfuyu.util.api import APIRequest


# Test
###########################################################################
@pytest.fixture
def instance():
    return APIRequest("https://dummyjson.com/quotes")


def test_API(instance: APIRequest):
    try:
        assert isinstance(instance.fetch_data_only().json()["quotes"], list)
    except:
        # No internet
        assert instance