"""
    Test of dictionaries_loader
"""
from textcorpus_generator.util.string_utils import standardization


def test1():
    result = standardization('(bla bla)')
    assert result == ''


def test2():
    result = standardization('(bla bla)\(truc)')
    assert result == ''

