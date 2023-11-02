"""
Test: Generator

Version: 1.0.0
Date updated: 25/05/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
import re
import string

import pytest

from absfuyu.collections.generator import Generator, Charset


# Test
###########################################################################
# Charset
def test_Charset():
    assert Charset.PRODUCT_KEY == "BCDFGHJKMNPQRTVWXY2346789"

def test_Charset_2():
    """[a-zA-Z0-9]"""
    assert Charset.DEFAULT == string.ascii_letters + string.digits


# generate_string
def test_generate_string():
    """Correct len and a list"""
    temp = Generator.generate_string(
        charset=Charset.DEFAULT,
        size=8,
        times=1,
        unique=False,
        string_type_if_1=False
    )
    assert isinstance(temp, list) and len(temp[0])==8

def test_generate_string_2():
    """Correct len and a str"""
    temp = Generator.generate_string(
        charset=Charset.DEFAULT,
        size=8,
        times=1,
        unique=False,
        string_type_if_1=True
    )
    assert isinstance(temp, str) and len(temp)==8

def test_generate_string_3():
    """Unique generate"""
    temp = Generator.generate_string(
        charset=Charset.DEFAULT,
        size=2,
        times=600,
        unique=True,
    )
    assert len(temp) == len(list(set(temp)))


# generate_key
def test_generate_key():
    """Check if key generate correctly"""
    key = Generator.generate_key(
        charset=Charset.PRODUCT_KEY,
        letter_per_block=5,
        number_of_block=5,
        sep="-"
    )
    key_pattern = r"[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}"
    check_result = re.search(key_pattern, key) # Correct default key pattern
    correct_len = len(key) == 29 # Correct default key length
    assert check_result is not None and correct_len


# generate_check_digit
def test_generate_check_digit():
    assert Generator.generate_check_digit(95489683516944151927) == 0

def test_generate_check_digit_2():
    assert Generator.generate_check_digit(15392479156575151882) == 1

def test_generate_check_digit_3():
    assert Generator.generate_check_digit(74662116892282572844) == 2

def test_generate_check_digit_4():
    assert Generator.generate_check_digit(91274812716671415644) == 3

def test_generate_check_digit_5():
    assert Generator.generate_check_digit(94984564168167844561) == 4

def test_generate_check_digit_6():
    assert Generator.generate_check_digit(94273419372476632513) == 5

def test_generate_check_digit_7():
    assert Generator.generate_check_digit(78985469454121383396) == 6

def test_generate_check_digit_8():
    assert Generator.generate_check_digit(34458526632449856638) == 7

def test_generate_check_digit_9():
    assert Generator.generate_check_digit(95486688921998713381) == 8

def test_generate_check_digit_10():
    assert Generator.generate_check_digit(48981383446354864289) == 9
