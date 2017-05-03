"""
    Tests of balancer
"""
import unittest

from textcorpus_generator.util.balancer import Balancer


class TestBalancer(unittest.TestCase):
    def test1(self):
        balancer = Balancer(["intent1", "intent2"], None)
        assert len(balancer.intents) == 2
        assert balancer.intents['intent1'] == 50.0
        assert balancer.intents['intent2'] == 50.0

    def test2(self):
        balancer = Balancer(["intent1", "intent2"], {"intent1": 30})
        assert len(balancer.intents) == 2
        assert balancer.intents['intent1'] == 30.0
        assert balancer.intents['intent2'] == 70.0

    def test3(self):
        balancer = Balancer(["intent1", "intent2"], {"intent1": 30, "intent3": 40})
        assert len(balancer.intents) == 2
        assert balancer.intents['intent1'] == 30.0
        assert balancer.intents['intent2'] == 70.0

    if __name__ == '__main__':
        unittest.main()
