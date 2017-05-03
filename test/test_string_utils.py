"""
    Tests of dictionaries_loader
"""
import unittest

from textcorpus_generator.util.string_utils import standardization


class TestStingUtils(unittest.TestCase):
    def test1(self):
        result = standardization('(bla bla)')
        assert result == ''

    def test2(self):
        result = standardization('(bla bla)\(truc)')
        assert result == ''

    if __name__ == '__main__':
        unittest.main()
