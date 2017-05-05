"""
Dictionnary Handler
Load dictionnaries in memory from a directory containing a list of dictionnaries

Dictionnary files follow the pattern "B-(.)+" or "X-(.)+)"
"""

import itertools
import logging
import os
from os import listdir
from os.path import isfile, join

from textcorpus_generator.util.string_utils import standardization


class DictionariesLoader:
    dictionaries = {}

    def __init__(self, dictionaries_path: str):

        self.logger = logging.getLogger(__name__)
        self.logger.info("Load dictionaries from {directory} ".format(directory=dictionaries_path))
        files = [f for f in listdir(dictionaries_path) if isfile(join(dictionaries_path, f)) if f.endswith('.csv')]
        # os.chdir(dictionaries_path)
        for file in files:
            self.process_file(os.path.join(dictionaries_path, file))

    def process_file(self, file_name):
        """
        Process a dictionary file
        :param file_name:
        """
        basename = os.path.basename(file_name)
        if basename.startswith("B-") or basename.startswith("X-"):
            dictionary = []
            self.logger.info("Load {} dictionnary".format(file_name))
            with open(file_name) as fp:
                dictionary_name = basename.replace('.csv', "")
                for line in fp:
                    dictionary.append(standardization(line))
                self.dictionaries[dictionary_name] = dictionary

    def get_iob_list(self):
        """
        Get a list of all the IOB tokens
        :return:
        """
        return ['O'] + list(
            itertools.chain.from_iterable(('B-' + dictionary, 'I-' + dictionary) for dictionary in self.get_labels_list()))

    def get_labels_list(self):
        """
        Get all the iob labels used in the templates
        :return:
        """
        labels = set(label[2:].split('#')[0] for label in self.dictionaries.keys() if label.startswith('B-'))

        return list(labels)

