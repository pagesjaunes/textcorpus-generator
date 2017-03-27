"""
    Text corpus generation

Usage:
    generate_corpus.py --templates=filepath --dictionaries=path --output_path=path [--iterations=int] [--debug]

Options:
    --help                  Displays help message
    --templates=filepath    Sets the path to the template file
    --dictionaries=path     Sets the path to the ditionaries file
    --output_path=path      Sets the path where to write the generated corpus
    --iterations=int        Iterations count on a template
    --debug                 Debug version of the script

"""
import random

import logging

import re
from docopt import docopt

from textcorpus_generator.commons import configuration, logger
from textcorpus_generator.util.dictionaries_loader import DictionariesLoader
from textcorpus_generator.util.template_loader import TemplateLoader

labeled_sentences = []


def pick_random_item_in_dictionary(token: str) -> str:
    dictionary = dictionaies_loader.dictionaries[token]
    if dictionary is None:
        return ""
    else:
        index = random.randint(0, len(dictionary) - 1)
        return dictionary[index]


def build_sentence_and_iob(template: str) -> str:
    sentence = []
    iob = []

    template = template.rstrip()
    if template.find("B-") > 0 or template.find("X-") > 0:
        tokens = template.split(' ')
        for token in tokens:
            if token.startswith("X-"):
                item = pick_random_item_in_dictionary(token)

                sentence.append(item)
                iob.append("O")

                nb_i_label = len(item.split(" ")) - 1
                while nb_i_label > 0:
                    iob.append("O")
                    nb_i_label -= 1
            elif token.startswith("B-"):
                item = pick_random_item_in_dictionary(token)

                # remove extensions ...
                token = re.sub('.dela$', '', token)
                token = re.sub('.du$', '', token)
                token = re.sub('.des$', '', token)
                token = re.sub('.le$', '', token)
                token = re.sub('.la$', '', token)
                token = re.sub('.un$', '', token)
                token = re.sub('.une$', '', token)
                token = re.sub('.ma$', '', token)
                token = re.sub('.mon$', '', token)

                sentence.append(item)
                iob.append(token)

                nb_i_label = len(item.split(" ")) - 1
                i_label = token.replace("B-", "I-")
                while nb_i_label > 0:
                    iob.append(i_label)
                    nb_i_label -= 1
            else:
                sentence.append(token)
                iob.append("O")

    if len(sentence) > 0:
        return ' '.join(sentence).lstrip() + ";" + ' '.join(iob)
    else:
        return ''


def process(output_path: str, nb_iterations: int):

    # Generate train corpus
    logger.info('Generate train corpus')
    for template in templates_loader.templates:
        parts = template.split(";")

        for iteration in range(0, nb_iterations):
            sentence_and_iob = build_sentence_and_iob(parts[0])
            if len(sentence_and_iob) > 0:
                labeled_sentences.append(sentence_and_iob + ';' + parts[1])

    # shuffle
    logger.info('Shuffle')
    random.shuffle(labeled_sentences)

    # generate files
    logger.info('Generate train outputs files')
    with open(output_path + '/sentences.txt', 'w') as f_sentence, open(output_path + '/iobs.txt', 'w') as f_iob, open(
                    output_path + '/intents.txt', 'w') as f_intent:
        for item in labeled_sentences:
            parts = item.split(';')
            f_sentence.write(parts[0] + '\n')
            f_iob.write(parts[1] + '\n')
            f_intent.write(parts[2] + '\n')


if __name__ == '__main__':
    conf = configuration.load()

    # Command line args
    # __doc__ contains the module docstring
    arguments = docopt(__doc__, version=conf['version'])

    if arguments['--debug']:
        conf['log']['level'] = 'DEBUG'

    logger.configure(conf['log']['level_values'][conf['log']['level']], conf['log']['dir'], conf['log']['filename'],
                     conf['log']['max_filesize'], conf['log']['max_files'])

    logger = logging.getLogger(__name__)

    dictionaies_loader = DictionariesLoader(arguments['--dictionaries'])
    templates_loader = TemplateLoader(arguments['--templates'])
    nb_iterations = arguments['--iterations']
    if nb_iterations is None:
        nb_iterations = 10  # default
    process(arguments['--output_path'], nb_iterations)

    print(labeled_sentences[0])
    print(labeled_sentences[1])
