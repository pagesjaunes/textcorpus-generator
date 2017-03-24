"""
    Test of utterance_expander
"""
from textcorpus_generator.util.utterance_expander import expand


def test1():
    array = expand('(hello|hi) (|mighty) world')
    assert array == ['hello mighty world', 'hello world', 'hi mighty world', 'hi world']


def test2():
    array = expand('hello (|mighty) world')
    assert array == ['hello mighty world', 'hello world']


def test3():
    array = expand('(great|good|nice) day')
    assert array == ['great day', 'good day', 'nice day']


def test4():
    array = expand("(when is|when's) the (|next) Dodger's (|baseball) game?")
    assert array == ["when is the next Dodger's baseball game?", "when is the next Dodger's game?",
                     "when is the Dodger's baseball game?", "when is the Dodger's game?",
                     "when's the next Dodger's baseball game?", "when's the next Dodger's game?",
                     "when's the Dodger's baseball game?", "when's the Dodger's game?"]


def test5():
    array = expand('(|hello) world')
    assert array == ['hello world', 'world']


def test7():
    array = expand('hello world')
    assert array == ['hello world']


def test8():
    array = expand('(hello)')
    assert array == ['hello']


def test9():
    array = expand('(hello) world')
    assert array == ['hello world']


def test10():
    array = expand('(B-alorscamarcheavecunBdevant) world')
    assert array == ['B-alorscamarcheavecunBdevant world']


def test11():
    array = expand('(b-truc) world')
    assert array == ['b-truc world']
