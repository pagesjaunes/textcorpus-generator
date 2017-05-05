"""
    Tests of Equalizer
"""
import unittest

from textcorpus_generator.util.equalizer import Equalizer


class TestEqualizer(unittest.TestCase):
    def test1(self):
        equalizer = Equalizer(["intent1", "intent2"], None)
        assert len(equalizer.intents) == 2
        assert equalizer.intents['intent1'] == 50.0
        assert equalizer.intents['intent2'] == 50.0

    def test2(self):
        equalizer = Equalizer(["intent1", "intent2"], {"intent1": 30})
        assert len(equalizer.intents) == 2
        assert equalizer.intents['intent1'] == 30.0
        assert equalizer.intents['intent2'] == 70.0

    def test3(self):
        equalizer = Equalizer(["intent1", "intent2"], {"intent1": 30, "intent3": 40})
        assert len(equalizer.intents) == 2
        assert equalizer.intents['intent1'] == 30.0
        assert equalizer.intents['intent2'] == 70.0

    if __name__ == '__main__':
        unittest.main()
