"""
Absfuyu: Data extension
---
Extension for data type such as `list`, `str`, ...

Version: 1.3.0
Date updated: 16/06/2023 (dd/mm/yyyy)

Features:
- Text
- ListKai
- DictKai
- IntNumber
"""


# Module level
###########################################################################
__all__ = [
    "Text", "IntNumber",
    "ListKai", "DictKai"
]


# Library
###########################################################################
from collections import Counter
from itertools import accumulate, chain, groupby
import math
import operator
import random
from typing import Any, Dict, List, Union

from absfuyu.collections.generator import Generator, Charset
from absfuyu.logger import logger, log_debug
from absfuyu.util import set_min, set_min_max


# Class
###########################################################################
class Text(str):
    """
    `str` extension
    """
    def divide(self, string_split_size: int = 60) -> list:
        """
        Summary
        -------
        Divide long string into smaller size

        Parameters
        ----------
        string_split_size : int
            divide string every x character
            (default: x = 60)

        Returns
        -------
        list
            A list in which each item is a smaller
            string with the size of string_split_size
            (need to be concaternate later)
        """
        temp = self
        output = []
        while len(temp) != 0:
            output.append(temp[:string_split_size])
            temp = temp[string_split_size:]
        return output
    
    def divide_with_variable(
            self,
            split_size: int = 60,
            split_var_len: int = 12,
            custom_var_name: Union[str, None] = None,
        ) -> list:
        """
        Summary
        -------
        Divide long string into smaller size,
        then assign a random variable to splited
        string for later use

        Parameters
        ----------
        split_size : int
            divide string every x character
            (default: x = 60)
        
        split_var_len : int
            length of variable name assigned to each item
            (default: 12)
        
        custom_var_name : str
            custom var name when join string

        Returns
        -------
        list
            A list in which each item is a smaller
            string with the size of split_size
            and a way to concaternate them (when using print)
        
        Example
        -------
        >>> ["qwerty","uiop"]

        ["asd='qwerty'","asx='uiop'","asw=asd+asx","asw"]
        """

        temp = self.divide(split_size)
        output = []
        
        # split variable
        splt_var_len = split_var_len
        splt_len = len(temp)

        if custom_var_name is None:
            splt_name = Generator.generate_string(
                charset=Charset.ALPHABET,
                size=split_var_len,
                times=splt_len+1
            )
            for i in range(splt_len):
                output.append(f"{splt_name[i]}='{temp[i]}'")
        else:
            for i in range(splt_len):
                output.append(f"{custom_var_name}{i+1}='{temp[i]}'")
        
        # joined variable
        temp = []
        if custom_var_name is None:
            for i in range(splt_len):
                if i == 0:
                    temp.append(f"{splt_name[-1]}=")
                if (i == splt_len-1):
                    temp.append(f"{splt_name[i]}")
                else:
                    temp.append(f"{splt_name[i]}+")
        else:
            for i in range(splt_len):
                if i == 0:
                    temp.append(f"{custom_var_name}=")
                if (i == splt_len-1):
                    temp.append(f"{custom_var_name}{i+1}")
                else:
                    temp.append(f"{custom_var_name}{i+1}+")
        
        output.append("".join(temp))
        if custom_var_name is None:
            output.append(splt_name[-1])
        else:
            output.append(custom_var_name)

        return output


    def analyze(self) -> dict:
        """
        Summary
        -------
        String analyze (count number of type of character)

        Returns
        -------
        dict
            A dictionary contains number of digit character,
            uppercase character, lowercase character, and
            special character
        """

        temp = self

        detail = {
            "digit": 0,
            "uppercase": 0,
            "lowercase": 0,
            "other": 0
        }

        for x in temp:
            if ord(x) in range(48, 58): #num
                detail["digit"] += 1
            elif ord(x) in range(65, 91): #cap
                detail["uppercase"] += 1
            elif ord(x) in range(97, 123): #low
                detail["lowercase"] += 1
            else:
                detail["other"] += 1
        
        return detail
    

    def reverse(self):
        """Reverse string"""
        return __class__(self[::-1])


    def is_pangram(self) -> bool:
        """
        Summary
        -------
        Check if string is a pangram

            A pangram is a unique sentence in which
            every letter of the alphabet is used at least once

        Returns
        -------
        bool
            True if string is a pangram
        """
        text = self
        alphabet = set("abcdefghijklmnopqrstuvwxyz")
        return not set(alphabet) - set(text.lower())

    def is_palindrome(self) -> bool:
        """
        Summary
        -------
        Check if string is a palindrome

            A palindrome is a word, verse, or sentence 
            or a number that reads the same backward or forward

        Returns
        -------
        bool
            True if string is a palindrome
        """
        text = self
        # Use string slicing [start:end:step]
        return text == text[::-1]
    
    def to_hex(self, raw: bool = False) -> str:
        r"""
        Summary
        -------
        Convert string to hex form

        Parameters
        ----------
        raw : bool
            False: hex string in the form of `\x` (default)
            True: normal hex string

        Returns
        -------
        str
            Hexed string
        """
        text = self
        
        byte_str = text.encode("utf-8")
        hex_str = byte_str.hex()
              
        if not raw:
            temp = []
            str_len = len(hex_str)

            for i in range(str_len):
                if i % 2 == 0:
                    temp.append(f"\\x")
                temp.append(hex_str[i])
            return "".join(temp)
        else:
            return hex_str

    def random_capslock(self, probability: int = 50):
        """
        Randomly capslock letter in string

        probability : int
            probability in range [0, 100]
            (default: 50)
        """
        probability = set_min_max(probability)
        text = self.lower()
        
        temp = []
        for x in text:
            if random.randint(1, 100) <= probability:
                x = x.upper()
            temp.append(x)
        logger.debug(temp)
        return __class__("".join(temp))


class IntNumber(int):
    """
    `int` extension
    """
    # convert stuff
    def to_binary(self) -> str:
        """Convert to binary number"""
        return format(self, "b")
    
    def to_celcius_degree(self) -> float:
        """
        Convert into Celcius degree as if `self` is Fahrenheit degree
        """
        c_degree = (self - 32) / 1.8
        return c_degree
    
    def to_fahrenheit_degree(self) -> float:
        """
        Convert into Fahrenheit degree as if `self` is Celcius degree
        """
        f_degree = (self * 1.8) + 32
        return f_degree


    # is_stuff
    def is_prime(self) -> bool:
        """
        Summary
        -------
        Check if the integer is a prime number or not

            A prime number is a natural number greater than 1
            that is not a product of two smaller natural numbers.
            A natural number greater than 1 that is not prime
            is called a composite number.

        Returns
        -------
        bool
            True if a prime number
        """
        number = self
        
        if int(number) <= 1:
            return False
        for i in range(2, int(math.sqrt(number)) + 1):# divisor range
            if (number % i == 0):
                return False
        return True
    
    def is_twisted_prime(self) -> bool:
        """
        A number is said to be twisted prime if
        it is a prime number and
        reverse of the number is also a prime number
        """
        prime = self.is_prime()
        logger.debug(f"is prime: {prime}")
        rev = self.reverse().is_prime()
        logger.debug(f"is prime when reversed: {rev}")
        return prime and rev
    
    def is_perfect(self) -> bool:
        """
        Summary
        -------
        Check if integer is perfect number

            Perfect number: a positive integer that is
            equal to the sum of its proper divisors.
            The smallest perfect number is 6, which is
            the sum of 1, 2, and 3.
            Other perfect numbers are 28, 496, and 8,128.

        Returns
        -------
        bool
            True if a perfect number
        """
        ###################################
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
            # 1_257_787, 1_398_269, 2_976_221, 3_021_377, 6_972_593,
            # 13_466_917, 20_996_011, 24_036_583, 25_964_951,
            # 30_402_457, 32_582_657, 37_156_667, 42_643_801,
            # 43_112_609, 57_885_161,
            ## 74_207_281, 77_232_917, 82_589_933
        ]
        perfect_number = []
        for x in perfect_number_index:
            # a perfect number have a form of (2**(n-1))*((2**n)-1)
            perfect_number.append((2**(x-1))*((2**x)-1))
        """
        number = self

        perfect_number = [
            6, 28, 496, 8128,
            33_550_336, 8_589_869_056,
            137_438_691_328,
            2_305_843_008_139_952_128
        ]
        
        if int(number) in perfect_number:
            return True
        
        elif int(number) < perfect_number[-1]:
            return False
        
        else:
            # Faster way to check
            perfect_number_index = [
                61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217,
                4253, 4423, 9689, 9941, 11_213, 19_937, 21_701, 23_209,
                44_497, 86_243, 110_503, 132_049, 216_091, 756_839,
                859_433, 1_257_787,
                # 1_398_269, 2_976_221, 3_021_377, 6_972_593,
                # 13_466_917, 20_996_011, 24_036_583, 25_964_951,
                # 30_402_457, 32_582_657, 37_156_667, 42_643_801,
                # 43_112_609, 57_885_161,
                ## 74_207_281, 77_232_917, 82_589_933
            ]
            for x in perfect_number_index:
            # a perfect number have a form of (2**(n-1))*((2**n)-1)
                perfect_number = ((2**(x-1))*((2**x)-1))
                if number < perfect_number:
                    return False
                elif number == perfect_number:
                    return True
            
            # Manual way when above method not working
            # sum
            s = 1
            # add all divisors
            i = 2
            while i * i <= number:
                if number % i == 0:
                    s += + i + number/i
                i += 1
            # s == number -> perfect
            return (True if s == number and number!=1 else False)

    def is_narcissistic(self) -> bool:
        """
        Check if a narcissistic number

            In number theory, a narcissistic number
            (also known as a pluperfect digital invariant (PPDI),
            an Armstrong number (after Michael F. Armstrong)
            or a plus perfect number) in a given number base `b`
            is a number that is the sum of its own digits
            each raised to the power of the number of digits.
        """
        check = sum([int(x) ** len(str(self)) for x in str(self)])
        return self == check

    def reverse(self):
        """Reverse a number"""
        return __class__(str(self)[::-1])
    
    def is_palindromic(self) -> bool:
        """
        A palindromic number (also known as a numeral palindrome
        or a numeric palindrome) is a number (such as 16461)
        that remains the same when its digits are reversed.
        """
        return self == self.reverse()
    
    def is_palindromic_prime(self) -> bool:
        """
        A palindormic prime is a number which is both palindromic and prime
        """
        return self.is_palindromic() and self.is_prime()
    

    # calculation stuff
    def lcm(self, with_number: int):
        """Least common multiple of `self` and `with_number`"""
        return __class__((self * with_number) // math.gcd(self, with_number))
    
    def add_to_one_digit(self, master_number: bool = False):
        """
        Convert `self` into 1-digit number by add all of the digits together

        master_number: bool
            Break when sum = 22 or 11 (numerology)
        """
        number = self
        logger.debug(f"Current number: {number}")
        while len(str(number)) != 1:
            number = sum(map(int, str(number)))
            if master_number:
                if number == 22 or number == 11:
                    break # Master number
            logger.debug(f"Sum after loop: {number}")
        return __class__(number)


class ListKai(list):
    """
    `list` extension
    """
    def stringify(self):
        """
        Summary
        -------
        Convert all item in list into string

        Returns
        -------
        list
            A list with all items with type: string
        """
        return ListKai(map(str, self))

    def sorts(self, reverse: bool = False):
        """
        Sort all items (with different type) in list
        
        Parameters
        ----------
        reverse : bool
            if True then sort in descending order

        Returns
        -------
        list
            A sorted list
        """
        lst = self.copy()
        type_weights = {}
        for x in lst:
            if type(x) not in type_weights:
                type_weights[type(x)] = len(type_weights)
        logger.debug(f"Type weight: {type_weights}")

        output = sorted(
            lst,
            key=lambda x: (type_weights[type(x)], str(x)),
            reverse=reverse
        )

        logger.debug(output)
        return __class__(output)
    
    def freq(
            self,
            sort: bool = False,
            num_of_first_char: int = None,
            appear_increment: bool = False
        ):
        """
        Find frequency of each item in list

        Parameters
        ----------
        sort : bool
            if True: sort the dict in ascending order
        
        num_of_first_char : int
            number of first character taken into account to sort
            (default: None)
            (num_of_first_char = 1: first character in each item)
        
        appear_increment : bool
            return incremental index list of each item when sort
            example:
            original: [1,1,2,3,3,4,5,6]
            appear_increment = [2, 3, 5, 6, 7, 8]

        Returns
        -------
        dict
            A dict that show frequency
        
        list
            Incremental index list
        """

        if sort:
            data = self.sorts()
        else:
            data = self.copy()
        
        if num_of_first_char is None:
            temp = Counter(data)
        else:
            max_char = min([len(str(x)) for x in data])
            logger.debug(f"Max character: {max_char}")
            if num_of_first_char not in range(1, max_char):
                logger.debug(f"Not in {range(1, max_char)}. Using default value...")
                temp = Counter(data)
            else:
                logger.debug(f"Freq of first {num_of_first_char} char")
                temp = Counter([str(x)[:num_of_first_char] for x in data])
        
        try:
            times_appear = dict(sorted(temp.items()))
        except:
            times_appear = dict(__class__(temp.items()).sorts())
        log_debug(times_appear)
        
        if appear_increment:
            times_appear_increment = list(accumulate(times_appear.values(), operator.add))
            log_debug(times_appear_increment)
            return times_appear_increment
        else:
            return times_appear

    def slice_points(self, points: list):
        """
        Slices a list at specific indices into constituent lists.
        """
        points.append(len(self))
        data = self.copy()
        # return [data[points[i]:points[i+1]] for i in range(len(points)-1)]
        return [data[i1:i2] for i1, i2 in zip([0]+points[:-1], points)]

    def pick_one(self):
        """Pick one random items from list"""
        if len(self) != 0:
            out = random.choice(self)
            logger.debug(out)
            return out
        else:
            logger.debug("List empty!")
            return None
    
    def len_items(self):
        """
        `len()` for every item in `list[str]`
        """
        out = ListKai([len(str(x)) for x in self])
        # out = ListKai(map(lambda x: len(str(x)), self))
        logger.debug(out)
        return out

    def mean_len(self):
        """Average length of every item"""
        out = sum(self.len_items())/len(self)
        logger.debug(out)
        return out
    
    def apply(self, func):
        """Apply function to each entry"""
        # return __class__(func(x) for x in self)
        return __class__(map(func, self))

    def unique(self):
        """Remove duplicates"""
        return __class__(set(self))
    
    def group_by_unique(self):
        """
        Group duplicated elements into list
        
        Example
        -------

        >>> test = ListKai([1, 2, 3, 1, 3, 3, 2])
        >>> test.group_by_unique()
        [[1, 1], [2, 2], [3, 3, 3]]
        """
        # Old
        # out = self.sorts().slice_points(self.freq(appear_increment=True))
        # return __class__(out[:-1])

        # New
        temp = groupby(self.sorts())
        return __class__([list(g) for _, g in temp])

    def group_by_pair_value(self, max_loop: int = 3) -> List[list]:
        """
        Assume each `list` in `list` is a pair value, 
        returns a `list` contain all paired value

        max_loop: times to run functions (minimum: 3)

        Example
        -------

        >>> [[1, 2], [2, 3], [4, 3], [5, 6]]
        [[1, 2, 3, 4], [5, 6]]

        >>> [[8, 3], [4, 6], [6, 3], [5, 2], [7, 2]]
        [[8, 3, 4, 6], [2, 5, 7]]

        >>> [["a", 4], ["b", 4], [5, "c"]]
        [["a", "b", 4], ["c", 5]]
        """

        iter = self.copy()

        # Init loop
        for _ in range(set_min(max_loop, min_value=3)):

            temp: Dict[Any, list] = {}
            # Make dict{key: all `item` that contains `key`}
            for item in iter:
                for x in item:
                    if temp.get(x, None) is None:
                        temp[x] = [item]
                    else:
                        temp[x].append(item)

            # Flatten dict.values
            for k, v in temp.items():
                temp[k] = list(set(chain(*v)))
            
            iter = list(temp.values())

        return list(x for x, _ in groupby(iter))


class DictKai(dict):
    """
    `dict` extension
    """
    def analyze(self):
        """
        Analyze all the key values (int, float) in dict then return highest/lowest index
        """
        try:
            dct = self.copy()

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

            logger.debug(output)
            return output
        
        except:
            err_msg = "Value must be int or float"
            logger.error(err_msg)
            raise ValueError(err_msg)
    
    def swap_items(self):
        """Swap keys with values"""
        return __class__(zip(self.values(), self.keys()))



# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)
