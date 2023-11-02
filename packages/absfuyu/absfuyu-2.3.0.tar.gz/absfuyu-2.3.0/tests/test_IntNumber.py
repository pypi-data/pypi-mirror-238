"""
Test: IntNumber

Version: 1.1.0
Date updated: 04/06/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
import pytest

from absfuyu.collections.data_extension import IntNumber


# Test
###########################################################################
@pytest.fixture
def num_a():
    return IntNumber(5)

@pytest.fixture
def num_b():
    return IntNumber(10)

@pytest.fixture
def num_prime():
    return IntNumber(79)


# operation
def test_operation_add(num_a: IntNumber, num_b: IntNumber):
    assert num_a + num_b == 15

def test_operation_subtract(num_a: IntNumber, num_b: IntNumber):
    assert num_a - num_b == -5

def test_operation_multiply(num_a: IntNumber, num_b: IntNumber):
    assert num_a * num_b == 50

def test_operation_divide(num_a: IntNumber, num_b: IntNumber):
    assert num_a / num_b == 0.5

def test_operation_compare(num_a: IntNumber, num_b: IntNumber):
    assert (num_a > num_b) is False


# binary
def test_to_binary(num_b: IntNumber):
    assert num_b.to_binary() == "1010"

def test_to_binary_2(num_b: IntNumber):
    assert num_b.to_binary() == format(10, "b")


# reverse
def test_reverse(num_b: IntNumber):
    assert num_b.reverse() == 1

def test_reverse_2(num_a: IntNumber):
    assert num_a.reverse() == 5

def test_reverse_3(num_prime: IntNumber):
    assert num_prime.reverse() == 97


# prime
def test_is_prime(num_prime: IntNumber):
    assert num_prime.is_prime() is True

def test_is_prime_2():
    assert IntNumber(33).is_prime() is False

def test_is_twisted_prime(num_prime: IntNumber):
    assert num_prime.is_twisted_prime() is True

def test_is_twisted_prime_2():
    """
    53 is prime
    35 is not prime
    """
    assert IntNumber(53).is_twisted_prime() is False

def test_is_palindromic_prime():
    assert IntNumber(797).is_palindromic_prime() is True

def test_is_palindromic_prime():
    assert IntNumber(97).is_palindromic_prime() is False


# perfect
def test_is_perfect():
    assert IntNumber(28).is_perfect() is True

def test_is_perfect_2():
    assert IntNumber(22).is_perfect() is False


# narcissistic
def test_is_narcissistic():
    assert IntNumber(46).is_narcissistic() is False

def test_is_narcissistic_2():
    assert IntNumber(371).is_narcissistic() is True


# palindromic
def test_is_palindromic():
    assert IntNumber(12321).is_palindromic() is True

def test_is_palindromic_2():
    assert IntNumber(1231).is_palindromic() is False


# degree
def test_to_celcius_degree(num_a: IntNumber):
    assert num_a.to_celcius_degree() == -15.0

def test_to_fahrenheit_degree(num_a: IntNumber):
    assert num_a.to_fahrenheit_degree() == 41.0


# lcm
def test_lcm(num_a: IntNumber):
    assert num_a.lcm(6) == 30


# add_to_one_digit
def test_add_to_one_digit(num_prime: IntNumber):
    assert num_prime.add_to_one_digit() == 7

def test_add_to_one_digit_2():
    assert IntNumber(119).add_to_one_digit(master_number=True) == 11

def test_add_to_one_digit_3():
    assert IntNumber(994).add_to_one_digit(master_number=True) == 22