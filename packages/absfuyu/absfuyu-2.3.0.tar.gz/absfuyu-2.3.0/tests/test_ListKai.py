"""
Test: ListKai

Version: 1.0.0
Date updated: 25/05/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
import pytest

from absfuyu.collections.data_extension import ListKai


# Test
###########################################################################
@pytest.fixture
def example():
    return ListKai([
        3, 8, 5,
        "Test", "String", "ABC",
        [1,2,3], [0,8,6]
    ])

@pytest.fixture
def example_2():
    return ListKai([
        "Test", "String", "ABC",
        "Tension", "Tent", "Strong"
    ])


# stringify
def test_stringify(example: ListKai):
    assert all([isinstance(x, str) for x in example.stringify()]) is True


# sorts
def test_sorts(example: ListKai):
    assert example.sorts() == [3, 5, 8, 'ABC', 'String', 'Test', [0, 8, 6], [1, 2, 3]]


# freq
def test_freq(example_2: ListKai):
    assert example_2.freq(sort=True) == {'ABC': 1, 'String': 1, 'Strong': 1, 'Tension': 1, 'Tent': 1, 'Test': 1}

def test_freq_2(example_2: ListKai):
    assert example_2.freq(sort=True, num_of_first_char=2) == {'AB': 1, 'St': 2, 'Te': 3}

def test_freq_3(example_2: ListKai):
    assert example_2.freq(sort=True, num_of_first_char=2, appear_increment=True) == [1, 3, 6]


# slice_points
def test_slice_points(example_2: ListKai):
    assert example_2.slice_points([1, 3]) == [['Test'], ['String', 'ABC'], ['Tension', 'Tent', 'Strong']]


# pick_one
def test_pick_one():
    """Empty list"""
    assert ListKai([]).pick_one() is None

def test_pick_one_2(example_2: ListKai):
    assert len([example_2.pick_one()]) == 1


# len_items
def test_len_items(example_2: ListKai):
    assert example_2.len_items() == [4, 6, 3, 7, 4, 6]


# mean_len
def test_mean_len(example_2: ListKai):
    assert example_2.mean_len() == 5.0


# apply
def test_apply(example: ListKai):
    assert example.apply(str) == example.stringify()


# unique
def test_unique():
    assert ListKai([1, 1, 1, 1]).unique() == [1]
