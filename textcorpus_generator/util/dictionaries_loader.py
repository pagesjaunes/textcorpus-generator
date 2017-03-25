import logging
import os
from os import listdir
from os.path import isfile, join

from textcorpus_generator.util.string_utils import standardization


class DictionariesLoader:
    dictionaries = {}

    def __init__(self, dictionaries_path: str):

        logger = logging.getLogger(__name__)
        logger.info("Load dictionaries from %s\n", dictionaries_path)
        files = [f for f in listdir(dictionaries_path) if isfile(join(dictionaries_path, f)) if f.endswith('.csv')]
        os.chdir(dictionaries_path)
        for file in files:
            self.process_file(file)

    def process_file(self, file_name):

        if file_name.startswith("B-") or file_name.startswith("X-"):
            dictionary = []
            with open(file_name) as fp:
                dictionary_name = file_name.replace('.csv', "")
                for line in fp:
                    dictionary.append(standardization(line.lstrip()))
                self.dictionaries[dictionary_name] = dictionary
