# -*- coding: utf-8 -*-
"""
Absfuyu: Performance
---
Performance Check

Version: 1.0.0
Date updated: 27/05/2023 (dd/mm/yyyy)

Feature:
- measure_performance
- var_check
- source_this
"""


# Module level
###########################################################################
__all__ = [
    # Wrapper
    "measure_performance",
    # Functions
    "var_check", "source_this"
]


# Library
###########################################################################
from functools import wraps as __wraps
from inspect import getsource as __source
from time import perf_counter as __perf_counter
import tracemalloc as __tracemalloc

from absfuyu.logger import logger


# Function
###########################################################################
def measure_performance(func):
    r"""
    Summary
    -------
    Measure performance of a function

    Usage
    -----
    Use this as the decorator (@measure_performance)
    """
    
    @__wraps(func)
    def wrapper(*args, **kwargs):
        # Start memory measure
        __tracemalloc.start()
        # Start time measure
        start_time = __perf_counter()
        # Run function
        func(*args, **kwargs)
        # Get memory stats
        current, peak = __tracemalloc.get_traced_memory()
        # Get finished time
        finish_time = __perf_counter()
        # End memory measure
        __tracemalloc.stop()
        
        # Print output
        # print(f'{"-"*40}')
        # print(f'Function: {func.__name__}')
        # #print(f'Method: {func.__doc__}')
        # print(f"Memory usage:\t\t {current / 10**6:.6f} MB")
        # print(f"Peak memory usage:\t {peak / 10**6:.6f} MB")
        # print(f'Time elapsed (seconds):\t {finish_time - start_time:.6f}')
        # print(f'{"-"*40}')
        
        stat = {
            "Function": func.__name__,
            "Memory usage": current / 10**6,
            "Peak memory usage": peak / 10**6,
            "Time elapsed (seconds)": finish_time - start_time,
        }
        out: bool = False
        
        print(f"""
        {"-"*40}
        Function: {stat["Function"]}
        Memory usage:\t\t {stat["Memory usage"]:,.6f} MB
        Peak memory usage:\t {stat["Peak memory usage"]:,.6f} MB
        Time elapsed (seconds):\t {stat["Time elapsed (seconds)"]:,.6f}
        {"-"*40}
        """)
        
        if out:
            return stat
        
    return wrapper


def var_check(variable):
    """Check a variable"""
    
    # Check class
    try:
        clss = [variable.__name__, type(variable)]
    except:
        clss = type(variable)

    output = dict()
    try:
        output = {
            "value": variable,
            "class": clss,
            "id": id(variable),
        }
    except:
        return None

    # Docstring
    try:
        lc = [ # list of Python data types
            str,
            int, float, complex,
            list, tuple, range,
            dict,
            set, frozenset,
            bool,
            bytes,bytearray, memoryview,
            type(None)
        ]
        if type(variable) in lc:
            pass
        else:
            docs = variable.__doc__
            output["docstring"] = docs
    except:
        pass

    # Output
    return output


def source_this(function) -> str:
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

    return __source(function)


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)