"""
Test: Path

Version: 1.0.0
Date updated: 27/05/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
import pytest

from absfuyu.core import CORE_PATH
from absfuyu.util.path import DirStructure


# Test
###########################################################################
@pytest.fixture
def instance():
    return DirStructure(source_path=CORE_PATH)


def test_DirStructure(instance: DirStructure):
    assert instance.list_structure(
        "__pycache__",
        ".pyc",
        "tempCodeRunnerFile.py",
        "__init__",
        "__main__"
    )