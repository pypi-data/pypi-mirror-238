import pytest
from absfuyu import fun


def test_zodiac():
    assert fun.zodiac_sign(1, 1) == "Capricorn"

def test_zodiac_2():
    assert fun.zodiac_sign(1, 1, zodiac13=True) == "Sagittarius"

