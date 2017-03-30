"""
Template loader

Loads templates in memory and makes them available for generation
"""
import logging

from textcorpus_generator.util.utterance_expander import expand


class TemplateLoader:
    templates = []

    def __init__(self, file_name: str):
        logger = logging.getLogger(__name__)
        logger.info("Load templates from {file}".format(file=file_name))

        with open(file_name) as fp:
            for line in fp:
                line = line.rstrip()
                if not line.startswith('#') and len(line) > 0:
                    self.templates.extend(expand(line))
        logger.info('Load {counter} templates'.format(counter=len(self.templates)))
