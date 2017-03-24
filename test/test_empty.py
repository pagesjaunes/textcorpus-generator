"""
    Test of ???
"""
from textcorpus_generator.util.utterance_expander import expand


def test1():
    array = expand('(hello|hi) (|mighty) world')
    assert array == ['hello mighty world', 'hello world', 'hi mighty world', 'hi world']


def test2():
    array = expand('hello (|mighty) world')
    assert array == ['hello mighty world', 'hello world', 'hi mighty world', 'hi world']



# print(expand('(great|good|nice) day'))
# print(expand("(when is|when's) the (|next) Dodger's (|baseball) game?"))
# print(expand('(|hello) world'))
# print(expand('hello world'))
# print(expand('(hello)'))
# print(expand('(hello) world'))
# print(expand('(B-alorscamarcheavecunBdevant) world'))
# print(expand('(b-truc) world'))
