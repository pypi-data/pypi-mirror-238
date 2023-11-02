# -*- coding: utf-8 -*-
"""
Absfuyu: Sort
---
Sort Module

Version: 1.2.1
Last update: 25/06/2023 (mm/dd/yyyy)

Contain:
- selection_sort
- insertion_sort
"""


# Module level
###########################################################################
__all__ = [
    "selection_sort","insertion_sort",
    #"alphabetAppear",
]


# Library
###########################################################################
from collections import Counter, namedtuple
from itertools import accumulate
import operator
from typing import Dict as __Dict, List as __List, Union as __Union

from absfuyu.logger import logger


# Functions
###########################################################################
def selection_sort(lst: list, reverse: bool = False) -> list:
    """
    Summary
    -------
    Sort the list with selection sort (bubble sort) algorithm
 
    Parameters
    ----------
    lst : list
        list that want to be sorted
    
    reverse : bool
        if True: sort in descending order
        if False: sort in ascending order
        (default: False)

    Returns
    -------
    list
        sorted list
    """

    if reverse: # descending order
        for i in range(len(lst)):
            for j in range(i+1, len(lst)):
                if lst[i] < lst[j]:
                    lst[i], lst[j] = lst[j], lst[i]
        return lst
        
    else: # ascending order
        for i in range(len(lst)):
            for j in range(i+1, len(lst)):
                if lst[i] > lst[j]:
                    lst[i], lst[j] = lst[j], lst[i]
        return lst

def insertion_sort(lst: list) -> list:
    """
    Summary
    -------
    Sort the list with insertion sort algorithm
 
    Parameters
    ----------
    lst : list
        list that want to be sorted
    
    Returns
    -------
    list
        sorted list (ascending order)
    """

    for i in range (1,len(lst)):
        key = lst[i]
        j = i-1
        while j>=0 and key < lst[j]:
            lst[j+1] = lst[j]
            j -= 1
        lst[j+1] = key
    return lst


def alphabetAppear_old(lst: __List[str],
    ) -> __List[__Union[__Dict[str, int],__List[int]]]:
    r"""
    Summary
    -------
    Make a dict that show the frequency of
    item name's first character in list
    in alphabet order
    
    For example:

    >>> ["apple","bee","book"]

    freq = {"a": 1, "b": 2}
 
    Parameters
    ----------
    lst : list
        list that want to be analyzed
    
    Returns
    -------
    list
        analyzed list (list[0])
        apperance incremental value index (list[1])
    """

    al_char = [x[0] for x in selection_sort(lst)]
    times_appear = dict()
    for x in al_char:
        if x in times_appear:
            times_appear[x] += 1
        else:
            times_appear[x] = 1
    
    times_appear_increment = []
    total = 0
    for x in times_appear.values():
        total += x
        times_appear_increment.append(total)

    # first item is character frequency
    # second item is incremental index list
    return [times_appear, times_appear_increment]

AlphabetAppearResult = namedtuple("AlphabetAppearResult", ["times_appear", "times_appear_increment"])

def alphabetAppear(
        iterable: list,
        num_of_char_sorted: int = 1
    ) -> AlphabetAppearResult:
    r"""
    Summary
    -------
    Make a dict that show the frequency of
    item name's first character in list
    in alphabet order
    
    For example:

    >>> ["apple","bee","book"]

    freq = {"a": 1, "b": 2}
 
    Parameters
    ----------
    iterable : list
        list that want to be analyzed
    
    num_of_char_sorted : int
        number of first character taken into account to sort
        (default: first character in each item)
    
    Returns
    -------
    list
        analyzed list (list[0])
        apperance incremental value index (list[1])
    """

    if not isinstance(num_of_char_sorted, int):
        logger.debug("num_of_char_sorted is not int")
        num_of_char_sorted = 1
    if num_of_char_sorted < 1:
        logger.debug("num_of_char_sorted < 1")
        num_of_char_sorted = 1
    if num_of_char_sorted > min([len(str(x)) for x in iterable]):
        logger.debug("num_of_char_sorted > item length")
        num_of_char_sorted = min([len(str(x)) for x in iterable])
    temp = Counter([str(x)[:num_of_char_sorted] for x in iterable])
    times_appear = dict(sorted(temp.items()))
    logger.debug(times_appear)
    
    temp = accumulate(times_appear.values(), operator.add)
    times_appear_increment = list(temp)
    logger.debug(times_appear_increment)

    # first item is character frequency
    # second item is incremental index list
    return AlphabetAppearResult(times_appear, times_appear_increment)


def linear_search(iterable: list, key):
    """
    If key is in the list returns its position in the list,
    otherwise returns -1.
    """
    for i, item in enumerate(iterable):
        if item == key:
            return i
    return -1

def binary_search(iterable: list, key):
    """
    Returns the position of key in the list if found, -1 otherwise.

    List must be sorted.
    """
    left = 0
    right = len(iterable) - 1
    while left <= right:
        middle = (left + right) // 2
        
        if iterable[middle] == key:
            return middle
        if iterable[middle] > key:
            right = middle - 1
        if iterable[middle] < key:
            left = middle + 1
    return -1


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)
