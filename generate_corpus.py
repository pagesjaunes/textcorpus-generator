"""
    Text corpus generation

Usage:
    generate_corpus.py --templates=filepath --dictionaries=path --output_path=path [--sentences=int] [--debug]

Options:
    --help                  Displays help message
    --templates=filepath    Sets the file path to the template file
    --dictionaries=path     Sets the path to the dictionary directory
    --output_path=path      Sets the path where to write the generated corpus
    --sentences=int         Number of generated sentences
    --debug                 Debug version of the script
"""

import os

from docopt import docopt

from textcorpus_generator.CorpusGenerator import CorpusGenerator
from textcorpus_generator.commons import configuration, logger
from textcorpus_generator.util.dictionaries_loader import DictionariesLoader
from textcorpus_generator.util.equalizer import Equalizer
from textcorpus_generator.util.template_loader import TemplateLoader

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

    dictionaries_loader = DictionariesLoader(os.path.join(script_dir, arguments['--dictionaries']))
    templates_loader = TemplateLoader(os.path.join(script_dir, arguments['--templates']))
    equalizer = Equalizer(templates_loader.intents)
    equalizer.display()

    # init corpus generator with parameters
    generator = CorpusGenerator(dictionaries_loader, templates_loader, equalizer)

    # process
    nb_sentences_to_generate = 100000
    if arguments['--sentences'] is not None:
        nb_sentences_to_generate = int(arguments['--sentences'])
    generator.generate_corpus(nb_sentences_to_generate)

    # generate files
    output_path = arguments['--output_path']
    generator.save_corpus(output_path)
