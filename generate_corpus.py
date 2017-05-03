"""
    Text corpus generation

Usage:
    generate_corpus.py --templates=filepath --dictionaries=path --output_path=path [--sentences=int] [--debug]

Options:
    --help                  Displays help message
    --templates=filepath    Sets the path to the template file
    --dictionaries=path     Sets the path to the dictionary directory
    --output_path=path      Sets the path where to write the generated corpus
    --sentences=int         Number of generated sentences
    --debug                 Debug version of the script
"""

import logging
import os
import random
import re

from docopt import docopt

from textcorpus_generator.commons import configuration, logger
from textcorpus_generator.util.balancer import Balancer
from textcorpus_generator.util.dictionaries_loader import DictionariesLoader
from textcorpus_generator.util.template_loader import TemplateLoader


def verify(sentence: str, iob: str) -> bool:
    tokens1 = sentence.split(" ")
    tokens2 = iob.split(" ")

    if len(tokens1) != len(tokens2):
        logger.error("Wrong number of tokens %d;%d : %s \n", len(tokens1), len(tokens2), sentence);
        return False

    return True


def pick_random_item_in_dictionary(token: str) -> str:
    """
    Get an item randomnly from a dictionnary

    :param token: A token that match a dictionnary (X- or B-)
    :return: A word taken randomly from the dictionnary, or an empty string it no matching dict found
    """
    if token not in dictionaries_loader.dictionaries:
        logger.warn("No matchning dicionnary for {token}".format(token=token))
        return ""

    dictionary = dictionaries_loader.dictionaries[token]
    index = random.randint(0, len(dictionary) - 1)
    return dictionary[index]


def build_sentence_and_iob(template: str) -> str:
    """
    From a given template, for each sentence :
     - replace "B-" and "X-" words by a set of words from the matching dictionnary
     - build the matching IOB pattern

    :param template: A sentence template containing B- and X- strings
    :return: A set of instanciated sentences and their corresponding IOB string
    """
    sentence = []
    iob = []

    # if template.find("B-") > 0 or template.find("X-") > 0:
    tokens = template.split(' ')
    for token in tokens:
        # X entities can be pick from a dictionnary but are tagged as "O" (IOB pattern)
        if token.startswith("X-"):
            item = pick_random_item_in_dictionary(token)

            sentence.append(item)
            iob.append("O")

            nb_i_label = len(item.split(" ")) - 1
            while nb_i_label > 0:
                iob.append("O")
                nb_i_label -= 1
        # B entities are picked from a dictionnary and tagged as B- (I-)*
        elif token.startswith("B-"):
            item = pick_random_item_in_dictionary(token)

            # 'B-' pattern may be artificially suffixed by stop words (deal with gender issue)
            # but we want a lonely entity for all the B- sharing the same prefix.
            # This removes artificial extension :
            token = re.sub('#.*$', '', token)

            sentence.append(item)
            iob.append(token)

            nb_i_label = len(item.split(" ")) - 1
            i_label = token.replace("B-", "I-")
            while nb_i_label > 0:
                iob.append(i_label)
                nb_i_label -= 1
        # Deals with "hard coded" words of the template
        else:
            sentence.append(token)
            iob.append("O")

    if len(sentence) > 0:
        part1 = ' '.join(sentence).lstrip()
        part2 = ' '.join(iob)
        if verify(part1, part2):
            return part1 + ";" + part2
    return ''


def process():
    # Generate train corpus
    logger.info('Generate train corpus')

    # iterate over intents
    for intent in balancer.intents:
        # select templates
        templates = templates_loader.get_templates_by_intents(intent)
        # calculate nb sentences are needed
        nb_sentences_needed = round(balancer.intents[intent] * nb_sentences_to_generate / 100)
        generate_sentences(templates, nb_sentences_needed)

    # shuffle
    logger.info('Shuffle')
    random.shuffle(labeled_sentences)

    # generate files
    sentence_file = os.path.join(output_path, 'sentences.txt')
    iob_file = os.path.join(output_path, 'iobs.txt')
    intents_file = os.path.join(output_path, 'intents.txt')
    logger.info('Generate train outputs files : {sentence}, {iob} and {intents}'.format(
        sentence=sentence_file, iob=iob_file, intents=intents_file))

    counter = 0
    with open(sentence_file, 'w') as f_sentence, open(iob_file, 'w') as f_iob, open(
            intents_file, 'w') as f_intent:
        for item in labeled_sentences:
            logger.debug("Process sentence : {}".format(item))
            parts = item.split(';')
            f_sentence.write(parts[0] + '\n')
            f_iob.write(parts[1] + '\n')
            f_intent.write(parts[2] + '\n')
            counter += 1

    logger.info('Generate {counter} sentences'.format(counter=counter))


def generate_sentences(templates, nb_sentences_needed):
    counter = 0

    while counter <= nb_sentences_needed:
        for template in templates:
            parts = template.split(";")

            sentence_and_iob = build_sentence_and_iob(parts[0])
            if len(sentence_and_iob) > 0:
                labeled_sentences.append(sentence_and_iob + ';' + parts[1])
                counter += 1


if __name__ == '__main__':
    conf = configuration.load()
    script_dir = os.path.dirname(__file__)

    # init corpus generator from parameters
    # Command line args
    # __doc__ contains the module docstring
    arguments = docopt(__doc__, version=conf['version'])

    if arguments['--debug']:
        conf['log']['level'] = 'DEBUG'

    logger.configure(conf['log']['level_values'][conf['log']['level']], conf['log']['dir'], conf['log']['filename'],
                     conf['log']['max_filesize'], conf['log']['max_files'])

    logger = logging.getLogger(__name__)

    labeled_sentences = []
    nb_sentences_to_generate = 100000

    dictionaries_loader = DictionariesLoader(os.path.join(script_dir, arguments['--dictionaries']))
    templates_loader = TemplateLoader(os.path.join(script_dir, arguments['--templates']))
    balancer = Balancer(templates_loader.intents)

    if arguments['--sentences'] is not None:
        nb_sentences_to_generate = int(arguments['--sentences'])

    output_path = arguments['--output_path']

    process()
