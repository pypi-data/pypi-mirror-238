"""
Absfuyu: Calculation
---
Use to calculate small thing

Version: 1.5.0
Date updated: 25/05/2023 (dd/mm/yyyy)
"""

# Module level
###########################################################################
__all__ = [
    "toCelcius", "toFahrenheit", "lcm", "add_to_one_digit"
]


# Library
###########################################################################
import math as __math

from absfuyu.core import Number as __Num


# Function
###########################################################################
def toCelcius(
        number: __Num,
        roundup: bool = True
    ) -> __Num:
    """
    Summary
    -------
    Convert Fahrenheit to Celcius

    Parameters
    ----------
    number : Number
        F degree
    
    roundup : bool
        round the figure to .2f if True
        (default: True)

    Returns
    -------
    Number
        C degree
    """

    c_degree = (number - 32) / 1.8
    if roundup:
        return round(c_degree,2)
    else:
        return c_degree

def toFahrenheit(
        number: __Num,
        roundup: bool = True
    ) -> __Num:
    """
    Summary
    -------
    Convert Celcius to Fahrenheit

    Parameters
    ----------
    number : Number
        C degree
    
    roundup : bool
        round the figure to .2f if True
        (default: True)

    Returns
    -------
    Number
        F degree
    """

    f_degree = (number * 1.8) + 32
    if roundup:
        return round(f_degree, 2)
    else:
        return f_degree
    

def lcm(a: int, b: int):
    """
    Summary
    -------
    Least common multiple of a and b

    Parameters
    ----------
    a : int
        First number
    
    b : int
        Second number
    
    Returns
    -------
    int
        lcm
    """

    return (a*b) // __math.gcd(a,b)


def add_to_one_digit(number: int, master_number: bool = False):
    """
    Convert int number into 1-digit number by add all of the digit together

    master_number: bool
        Break when sum = 22 or 11 (numerology)
    """
    try: number = int(number)
    except: raise SyntaxError("Must be a number")

    while len(str(number)) != 1:
        number = sum([int(x) for x in str(number)])
        if master_number:
            if number == 22 or number == 11:
                break # Master number
    return number


# Run
###########################################################################
if __name__ == "__main__":
    pass