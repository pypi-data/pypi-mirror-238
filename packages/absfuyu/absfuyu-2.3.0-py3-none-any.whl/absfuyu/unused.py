"""
Absfuyu: Unused
---
Unused or obsoleted stuffs

Version: 1.0.0
Last update: 19/04/2023 (mm/dd/yyyy)
"""


# Library
###########################################################################
from dataclasses import dataclass, field
from inspect import getsource as __src
from typing import (
    Any as __Any,
    List as __List,
    Union as __Union,
    Dict as __Dict
)

from absfuyu.core import (
    Number as __Num,
)
from absfuyu.logger import logger
from absfuyu import sort


################################
# to documenting
"""
Summary
-------

Summary line.

Extended description of function.

Parameters
----------
arg1 : int
    Description of arg1

arg2 : str
    Description of arg2

Returns
-------
int
    Description of return value

"""
################################


# Function
###########################################################################
def matsum(
    matrix: __List[__Num],
    sum_opt: str = "all",
    ) -> __Union[__Num, __List[__Num], None]:
    """
    Summary
    -------
    Sum the elements in a matrix

    Parameters
    ----------
    matrix : list
        2 dimension list
    
    sum_opt : str
        "all": sum all the elements (default)
        "row": sum all the elements in each row
        "col": sum all the elements in each column

    Returns
    -------
    int or float
        "all" option
    list
        other options
    None
        when invalid option
    """

    sum_option = ["all", "row", "col"]

    if sum_opt not in sum_option:
        return None

    row = len(matrix)
    col = len(matrix[0])

    if (sum_opt == "all"):
        mat_sum = 0
        for i in range(row):
            for j in range(col):
                mat_sum += matrix[i][j]
        return mat_sum

    elif (sum_opt == "row"):
        mat_sum_row = []
        for i in range(row):
            srow = 0
            for j in range(col):
                srow += matrix[i][j]
            mat_sum_row.append(srow)
        return mat_sum_row

    elif (sum_opt == "col"):
        mat_sum_col = []
        for i in range(col):
            scol = 0
            for j in range(row):
                scol += matrix[j][i]
            mat_sum_col.append(scol)
        return mat_sum_col
    else:
        return None


def __isPerfectLegacy(number: int) -> bool:
    """
    A legacy function since the other runs faster
    """
    perfect_number = [6,28,496,8128,33550336,8589869056,
                      137438691328,2305843008139952128]
    if int(number) in perfect_number: return True
    elif int(number) < perfect_number[-1]: return False
    else:
        divisor = 1
        for i in range(2,int(number/2)+1):
            if (number%i == 0): divisor += i
        if number == divisor: return True
        else: return False


##############################################################
def unique_list(lst: list) -> list:
    """
    Summary
    -------
    Remove duplicate items in list

    Parameters
    ----------
    lst : list
        List that needs "cleaning"

    Returns
    -------
    list
        list that has no duplicates
    """
    return list(set(lst))


##############################################################
def reverse_number(number: __Num) -> __Num:
    """
    Reverse a number
    
    Parameters
    ----------
    number : int or float
        a number
    
    Returns
    -------
    A reversed number
    """
    
    # Try to convert from str to float
    if isinstance(number, str):
        try:
            number = float(number)
        except:
            raise ValueError("Must be a number")
    
    # Type: int
    if isinstance(number, int):
        return int(str(number)[::-1])
    
    # Type: float
    elif isinstance(number, float):
        if str(number).endswith(".0"): # normal number
            return int(str(str(number)[:-2])[::-1]) # remove decimals
        else:
            return float(str(number)[::-1])
    
    # Invalid number
    else:
        raise ValueError("Must be a number")


##############################################################
def fibonacci(number: int) -> int:
    """
    Summary
    -------
    Return a fibonacii number at the k-th position

    Parameters
    ----------
    number : int
        k-th position

    Returns
    -------
    int
        fibonacci number at the k-th position
    None
        Invalid value (k <= 0)
    """

    a = 0
    b = 1
    
    # number < 0
    if number < 0:
        return None
    
    # number = 0
    elif number == 0:
        return 0
    
    # number = 1
    elif number == 1:
        return b
    
    else:
        for _ in range(1, number):
            c = a+b
            a,b = b,c
        return b

def fibonacci_list(number: int):
    """
    Summary
    -------
    Return a fibonacii list from 0 to the k-th position

    Parameters
    ----------
    number : int
        k-th position

    Returns
    -------
    list[int]
        fibonacci number at the k-th position
    None
        Invalid value (k <= 0)
    """

    if number <= 0:
        return None
    
    fibLst = [0, 1]
    if number > 2:
        for i in range (2, number+1):
            fibLst.append(fibLst[i-1] + fibLst[i-2])
    return fibLst


##############################################################
def dict_int_analyze(dct: __Dict[str, __Num]):
    """
    Analyze all the key values (int, float) in dict then return highest/lowest index
    """

    input_ = list(dct.items())
    max, min = input_[0][1], input_[0][1]
    max_index = []
    min_index = []
    max_list = []
    min_list = []

    for i in range(len(input_)):
        if input_[i][1] > max:
            max = input_[i][1]
        elif input_[i][1] < min:
            min = input_[i][1]
    
    for i in range(len(input_)):
        if input_[i][1] == max:
            max_index.append(i)
        elif input_[i][1] == min:
            min_index.append(i)
    
    for x in max_index:
        max_list.append(input_[x])

    for x in min_index:
        min_list.append(input_[x])

    
    output = {
        "max_index": max_index,
        "min_index": min_index,
        "max": max_list,
        "min": min_list
    }

    return output

def dict_int_analyze_fast(dct: __Dict[str, __Num]):
    """
    Analyze all the key values (int, float) in dict then return highest/lowest index
    (faster version)
    """

    max_val = max(list(dct.values()))
    min_val = min(list(dct.values()))
    max_list = []
    min_list = []

    for k, v in dct.items():
        if v == max_val:
            max_list.append((k, v))
        if v == min_val:
            min_list.append((k, v))

    output = {
        "max_value": max_val,
        "min_value": min_val,
        "max": max_list,
        "min": min_list
    }

    return output


##############################################################
def stringify(lst: list) -> __List[str]:
    """
    Summary
    -------
    Convert all item in list into string

    Parameters
    ----------
    lst : list
        list of item

    Returns
    -------
    list
        A list with all items with type: string
    """

    return [str(x) for x in lst]

def list_sort(lst: __List[__Any], reverse: bool = False) -> list:
    """
    Summary
    -------
    Sort all items (with different type) in list
    
    Parameters
    ----------
    lst : list
        list of item
    
    reverse : bool
        if True then sort in descending order

    Returns
    -------
    list
        A sorted list
    """
    
    type_weights = {}
    for x in lst:
        if type(x) not in type_weights:
            type_weights[type(x)] = len(type_weights)
    output = sorted(
        lst,
        key=lambda x: (type_weights[type(x)], str(x)),
        reverse=reverse
    )
    return output

def list_freq(
        lst: __List[__Any],
        sort: bool = False,
    ) -> __Dict[str,int]:
    """
    Summary
    -------
    Find frequency of each item in list

    Parameters
    ----------
    lst : list
        list of item
    
    sort : bool
        if True: sort the dict in ascending order

    Returns
    -------
    dict
        A dict that show frequency
    """

    output = {}
    if sort:
        data = list_sort(lst)
    else:
        data = lst

    for x in data:
        if x not in output:
            output[x] = 1
        else:
            output[x] += 1
    return output


##############################################################
def srcMe(function) -> str:
    """
    Summary
    -------
    Show the source code of a function

    Parameters
    ----------
    function : Any
        just input the function name

    Returns
    -------
    Source code
    """

    return __src(function)


def __printAlphabet(lst: list):
    """
    Print item in list in alphabet order with line break
    """
    
    data = sort.alphabetAppear(lst)
    incre = data[1]
    for i in range(len(lst)):
        if i in incre:
            print("")
        if i == len(lst)-1:
            print(lst[i], end = " ")
        else:
            print(lst[i], end = "; ")
    
    return None


# Class
###########################################################################
@dataclass
class Dummy2:
    """
    Test class, will learn dataclass soon
    """
    attr1: int = field(default_factory=int)
    atrr2: int = field(default=10)


class Number:
    """Some common numbers"""    
    # 01
    @staticmethod
    def PerfectNumber(order: int) -> int:
        """
        Summary
        -------
        Perfect number: a positive integer that is
        equal to the sum of its proper divisors.
        The smallest perfect number is 6, which is
        the sum of 1, 2, and 3.
        Other perfect numbers are 28, 496, and 8,128.

        Parameters
        ----------
        order : int
            k-th position of perfect number

        Returns
        -------
        int
            Perfect number at k-th position
        """

        # List of known perfect number
        # Source: https://en.wikipedia.org/wiki/List_of_Mersenne_primes_and_perfect_numbers
        perfect_number_index = [
            2, 3, 5, 7,
            13, 17, 19, 31, 61, 89,
            107, 127, 521, 607,
            1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941,
            11_213, 19_937, 21_701, 23_209, 44_497, 86_243,
            110_503, 132_049, 216_091, 756_839, 859_433,
            1_257_787, 1_398_269, 2_976_221, 3_021_377, 6_972_593,
            13_466_917, 20_996_011, 24_036_583, 25_964_951,
            30_402_457, 32_582_657, 37_156_667, 42_643_801,
            43_112_609, 57_885_161,
            ## 74_207_281, 77_232_917, 82_589_933
        ]
        if order is None:
            return None
        elif order < 1 or order > len(perfect_number_index):
            return None
        else:
            idx = perfect_number_index[order-1]
            perfect_number = (2**(idx-1))*((2**idx)-1)
            return perfect_number
    
    # 02
    @staticmethod
    def PrimeNumber(order: int) -> int:
        r"""
        Summary
        -------
        Generate prime number at k-th position

        Parameters
        ----------
        order : int
            k-th position of prime number

        Returns
        -------
        int
            Prime number at k-th position
        
        Notes
        -----
        Still missing some number
        """

        if order is None or order < 1:
            return None
        
        prime_number = [
            2, 3, 5, 7, 11, 13, 17, 19,
            23, 29, 31, 37, 41,
        ]
        #order -= 1
        
        if order <= len(prime_number):
            return prime_number[order-1]
        else:
            order -= len(prime_number)
            prime = order**2 + order + 41
            return prime


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)