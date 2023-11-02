"""
Test: Converter

Version: 1.0.0
Date updated: 27/05/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
import pytest

from absfuyu.tools.converter import Text2Chemistry


# Test
###########################################################################
@pytest.fixture
def instance():
    return Text2Chemistry()


# convert
def test_convert(instance: Text2Chemistry):
    """Unvailable character"""
    assert instance.convert("jump") == []

def test_convert_2(instance: Text2Chemistry):
    """Unvailable character"""
    assert instance.convert("queen") == []

def test_convert_3(instance: Text2Chemistry):
    """Work"""
    assert instance.convert("bakery") != []

