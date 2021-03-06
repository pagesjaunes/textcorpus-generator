import logging


class Equalizer:
    """
    Equalizer is used too harmonise the intents distribution.

    Args:
        intents (list of str) : intents list.
        requirements (dictionary of str) : percent requirements.
    """

    intents = {}

    def __init__(self, intents, requirements=None):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Init Equalizer")

        # init
        for intent in intents:
            self.intents[intent] = None

        # set requirements
        somme = 0
        if requirements is not None:
            for intent, value in requirements.items():
                if intent in intents:
                    self.intents[intent] = value
                    somme += value
                else:
                    self.logger.warning("Unknown intent {}".format(intent))

        # set intents without requirements
        nb_itents_without_requirements = 0
        for intent in self.intents:
            if self.intents[intent] is None:
                nb_itents_without_requirements += 1

        for intent in self.intents:
            if self.intents[intent] is None:
                self.intents[intent] = (100 - somme) / nb_itents_without_requirements

    def display(self):
        for intent, value in self.intents.items():
            self.logger.info("{intent} -> {value} %".format(intent=intent, value=float("{0:.2f}".format(value))))
