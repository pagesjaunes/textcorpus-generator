"""
    Text corpus generation

Usage:
    generate_corpus.py --templates=filepath --dictionaries=path --output_path=path [--utterance=int] [--debug]

Options:
    --help                  Displays help message
    --templates=filepath    Sets the path to the template file
    --dictionaries=path     Sets the path to the dictionary directory
    --output_path=path      Sets the path where to write the generated corpus
    --utterance=int         Number of utterances over a template for a given
    --debug                 Debug version of the script

"""
import logging
import os
import random
import re

from docopt import docopt

from textcorpus_generator.commons import configuration, logger
from textcorpus_generator.util.dictionaries_loader import DictionariesLoader
from textcorpus_generator.util.template_loader import TemplateLoader

labeled_sentences = []


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
    dictionary = dictionaries_loader.dictionaries[token]
    if dictionary is None:
        logger.warn("No matchning dicionnary for {token}".format(token=token))
        return ""
    else:
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

    if template.find("B-") > 0 or template.find("X-") > 0:
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


def process(output_path: str, nb_utterance: int):
    # Generate train corpus
    logger.info('Generate train corpus')
    for template in templates_loader.templates:
        parts = template.split(";")

        for iteration in range(0, nb_utterance):
            sentence_and_iob = build_sentence_and_iob(parts[0])
            if len(sentence_and_iob) > 0:
                labeled_sentences.append(sentence_and_iob + ';' + parts[1])

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


if __name__ == '__main__':
    conf = configuration.load()
    script_dir = os.path.dirname(__file__)

    # Command line args
    # __doc__ contains the module docstring
    arguments = docopt(__doc__, version=conf['version'])

    if arguments['--debug']:
        conf['log']['level'] = 'DEBUG'

    logger.configure(conf['log']['level_values'][conf['log']['level']], conf['log']['dir'], conf['log']['filename'],
                     conf['log']['max_filesize'], conf['log']['max_files'])

    logger = logging.getLogger(__name__)

    dictionaries_loader = DictionariesLoader(os.path.join(script_dir, arguments['--dictionaries']))
    templates_loader = TemplateLoader(os.path.join(script_dir, arguments['--templates']))
    if arguments['--utterance'] is None:
        nb_utterances = 10
    else:
        nb_utterances = int(arguments['--utterance'])
    process(arguments['--output_path'], nb_utterances)
