"""
Absfuyu: Generator
---
This generate stuff (Not python's generator)

Version: 1.0.2
Date updated: 25/05/2023 (dd/mm/yyyy)

Features:
- Generate random string
- Generate key
- Generate check digit
"""


# Module level
###########################################################################
__all__ = [
    "Charset",
    "Generator"
]


# Library
###########################################################################
from random import choice
import string

from absfuyu.logger import logger, log_debug


# Class
###########################################################################
class Charset:
    """
    Character set data class
    """
    DEFAULT = string.ascii_letters + string.digits
    ALPHABET = string.ascii_letters
    FULL = string.ascii_letters + string.digits + string.punctuation
    UPPERCASE = string.ascii_uppercase
    LOWERCASE = string.ascii_lowercase
    DIGIT = string.digits
    SPECIAL = string.punctuation
    ALL = string.printable
    PRODUCT_KEY = "BCDFGHJKMNPQRTVWXY2346789" # Charset that various key makers use

    def __str__(self) -> str:
        charset = [x for x in __class__.__dict__.keys() if not x.startswith("__")]
        return f"List of Charset: {charset}"
    def __repr__(self) -> str:
        return self.__str__()


class Generator:
    """
    Generator class
    """
    def __init__(self) -> None:
        logger.debug("Class initiated!")
    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"
    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def generate_string(
            charset: str = Charset.DEFAULT,
            size: int = 8,
            times: int = 1,
            unique: bool = False,
            string_type_if_1: bool = False
        ):
        """
        Summary
        -------
        Generate a list of random string from character set (Random string generator)
        
        Parameters
        ----------
        charset : str
            - `Charset.DEFAULT`: character in [a-zA-Z0-9] (default)
            - `Charset.ALPHABET`: character in [a-zA-Z]
            - `Charset.FULL`: character in [a-zA-Z0-9] + special characters
            - `Charset.UPPERCASE`: character in [A-Z]
            - `Charset.LOWERCASE`: character in [a-z]
            - `Charset.DIGIT`: character in [0-9]
            - `Charset.SPECIAL`: character in [!@#$%^&*()_+=-]
            - `Charset.ALL`: character in every printable character
        
        size : int
            length of each string in list
        
        times : int
            how many random string generated
        
        unique : bool
            each generated text is unique
        
        string_type_if_1 : bool
            return a str type result if times == 1
            (default: False)
        
        Returns
        -------
        list
            list of random string generated
        str
            when string_type_if_1 is True
        None
            when invalid option
        """

        try:
            char_lst = list(charset)
        except:
            char_lst = charset
        # logger.debug(char_lst)

        unique_string = []
        count = 0
        logger.debug(f"Unique generated text: {unique}")

        while (count < times):
            s = "".join(choice(char_lst) for _ in range(size))
            logger.debug(f"Time generated: {count+1}. Remaining: {times-count-1}. {s}")
            if not unique:
                unique_string.append(s)
                count += 1
            else:
                if s not in unique_string:
                    unique_string.append(s)
                    count += 1
        
        logger.debug(log_debug(unique_string))
        if string_type_if_1 and times == 1:
            return unique_string[0]
        else:
            return unique_string
    
    @staticmethod
    def generate_key(
            charset: str = Charset.PRODUCT_KEY,
            letter_per_block: int = 5,
            number_of_block: int = 5,
            sep: str = "-"
        ):
        """
        charset: Character set
        letter_per_block: number of letter per key block
        number_of_block: number of key block
        sep: key block separator
        """
        out = sep.join(
            __class__.generate_string(charset, letter_per_block,
                                      number_of_block, False, False)
        )
        logger.debug(out)
        return out

    @staticmethod
    def generate_check_digit(number: int) -> int:
        """
        Summary
        -------
        Check digit generator
        
            "A check digit is a form of redundancy check used for
            error detection on identification numbers, such as
            bank account numbers, which are used in an application
            where they will at least sometimes be input manually.
            It is analogous to a binary parity bit used to
            check for errors in computer-generated data.
            It consists of one or more digits (or letters) computed
            by an algorithm from the other digits (or letters) in the sequence input.
            With a check digit, one can detect simple errors in
            the input of a series of characters (usually digits)
            such as a single mistyped digit or some permutations
            of two successive digits." (Wikipedia)
            
            This function use Luhn's algorithm to calculate
        
        Parameters
        ----------
        number : int
            base number to calculate check digit
        
        Returns
        -------
        int
            check digit
        """

        logger.debug(f"Base: {number}")
        # turn into list then reverse the order
        num = list(str(number))[::-1]
        sum = 0
        logger.debug(f"Reversed: {''.join(num)}")
        for i in range(len(num)):
            # convert back into integer
            num[i] = int(num[i])
            if i%2 == 0:
                # double value of the even-th digit
                num[i] *= 2
                # sum the character of digit if it's >= 10
                if num[i] >= 10:
                    num[i] -= 9
            sum += num[i]
            logger.debug(f"Loop {i+1}: {num[i]}, {sum}")
        
        out = (10 - (sum % 10)) % 10
        logger.debug(f"Output: {out}")
        return out


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10) # DEBUG