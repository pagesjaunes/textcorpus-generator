"""
    Text corpus generation

Usage:
    generate_corpus.py --template=filepath --output_path=dirpath [--debug]

Options:
    --help                  Displays help message
    --version               Displays the version number
    --template=filepath     Sets the path to the template file
    --output_path=filepath  Sets the path where to write the generated corpus
    --debug                 Debug version of the script

"""

from docopt import docopt
from textcorpus_generator.commons import configuration, logger




def process() :
    logger.info("\nCorpus generator " + arguments)

    # Generate train outputs Path

    # Generate validation outputs

    # Generate test outputs


if __name__ == '__main__':
    conf = configuration.load()

    # Command line args
    # __doc__ contains the module docstring
    arguments = docopt(__doc__, version=conf['version'])

    if arguments['--debug']:
        conf['log']['level'] = 'DEBUG'

    logger.configure(conf['log']['level_values'][conf['log']['level']], conf['log']['dir'], conf['log']['filename'], conf['log']['max_filesize'], conf['log']['max_files'])

