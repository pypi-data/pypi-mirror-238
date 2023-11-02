"""
Test: DictKai

Version: 1.0.0
Date updated: 25/05/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
import pytest

from absfuyu.collections.data_extension import DictKai


# Test
###########################################################################
@pytest.fixture
def example():
    return DictKai({
        "Line 1": 99,
        "Line 2": 50
    })


# analyze
def test_analyze(example: DictKai):
    assert example.analyze() == {'max_value': 99, 'min_value': 50, 'max': [('Line 1', 99)], 'min': [('Line 2', 50)]}

def test_analyze_2():
    """When values are not int or float"""
    ...


# swap
def test_swap(example: DictKai):
    assert example.swap_items() == {99: 'Line 1', 50: 'Line 2'}

