"""
    Tests of utterance_expander
"""
import unittest

from textcorpus_generator.util.utterance_expander import expand


class TestStringUtils(unittest.TestCase):
    def test1(self):
        array = expand('(hello|hi) (|mighty) world')
        assert array == ['hello mighty world', 'hello world', 'hi mighty world', 'hi world']

    def test2(self):
        array = expand('hello (|mighty) world')
        assert array == ['hello mighty world', 'hello world']

    def test3(self):
        array = expand('(great|good|nice) day')
        assert array == ['great day', 'good day', 'nice day']

    def test4(self):
        array = expand("(when is|when's) the (|next) Dodger's (|baseball) game?")
        assert array == ["when is the next Dodger's baseball game?", "when is the next Dodger's game?",
                         "when is the Dodger's baseball game?", "when is the Dodger's game?",
                         "when's the next Dodger's baseball game?", "when's the next Dodger's game?",
                         "when's the Dodger's baseball game?", "when's the Dodger's game?"]

    def test5(self):
        array = expand('(|hello) world')
        assert array == ['hello world', 'world']

    def test7(self):
        array = expand('hello world')
        assert array == ['hello world']

    def test8(self):
        array = expand('(hello)')
        assert array == ['hello']

    def test9(self):
        array = expand('(hello) world')
        assert array == ['hello world']

    def test10(self):
        array = expand('(B-alorscamarcheavecunBdevant) world')
        assert array == ['B-alorscamarcheavecunBdevant world']

    def test11(self):
        array = expand('(b-truc) world')
        assert array == ['b-truc world']

    if __name__ == '__main__':
        unittest.main()