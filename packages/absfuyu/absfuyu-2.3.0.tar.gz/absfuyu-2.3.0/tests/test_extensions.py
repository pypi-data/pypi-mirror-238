import pytest
from absfuyu import extensions as ext

def test_ext_load():
    assert ext.isloaded() is True