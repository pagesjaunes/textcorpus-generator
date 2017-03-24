"""
    Test of dictionaries_loader
"""
from textcorpus_generator.util.dictionaries_loader import standardization


def test1():
    result = standardization('(bla bla)')
    assert result == 'bla bla'


def test2():
    result = standardization('(bla bla) (truc)')
    assert result == 'bla bla truc'
