import logging
import os
import random
import re


class CorpusGenerator:
    logger = None

    labeled_sentences = []

    dictionaries_loader = None
    templates_loader = None
    equalizer = None

    def verify(self, sentence: str, iob: str) -> bool:
        """
        Verify if the input sentence and the iob has the same number of tokens
        :param sentence: sentence to verify
        :param iob: iob to verify
        :return: True if test is ok, False else
        """
        tokens1 = sentence.split(" ")
        tokens2 = iob.split(" ")

        if len(tokens1) != len(tokens2):
            self.logger.error("Wrong number of tokens %d;%d : %s \n", len(tokens1), len(tokens2), sentence);
            return False

        return True

    def pick_random_item_in_dictionary(self, token: str) -> str:
        """
        Get an item randomly from a dictionary

        :param token: A token that match a dictionary (X- or B-)
        :return: A word taken randomly from the dictionary, or an empty string it no matching dict found
        """
        if token not in self.dictionaries_loader.dictionaries:
            self.logger.warn("No matching dictionary for {token}".format(token=token))
            return ""

        dictionary = self.dictionaries_loader.dictionaries[token]
        index = random.randint(0, len(dictionary) - 1)
        return dictionary[index]

    def build_sentence_and_iob(self, template: str) -> str:
        """
        From a given template, build a sentence :
         - replace "B-" and "X-" words by a set of words from the matching dictionnary
         - build the matching IOB pattern

        :param template: A sentence template containing B- and X- strings
        :return: A set of instanciated sentences and their corresponding IOB string
        """
        sentence = []
        iob = []

        tokens = template.split(' ')
        for token in tokens:
            # X entities can be pick from a dictionnary but are tagged as "O" (IOB pattern)
            if token.startswith("X-"):
                item = self.pick_random_item_in_dictionary(token)

                sentence.append(item)
                iob.append("O")

                nb_i_label = len(item.split(" ")) - 1
                while nb_i_label > 0:
                    iob.append("O")
                    nb_i_label -= 1
            # B entities are picked from a dictionary and tagged as B- (I-)*
            elif token.startswith("B-"):
                item = self.pick_random_item_in_dictionary(token)

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

            #
            if self.verify(part1, part2):
                return part1 + ";" + part2

        return ''

    def generate_sentences(self, templates, nb_sentences_needed):
        """
        Generate sentences in the list labeled_sentences from a list of templates
        :param templates:
        :param nb_sentences_needed:
        :return:
        """
        counter = 0

        while counter <= nb_sentences_needed:
            for template in templates:
                parts = template.split(";")

                sentence_and_iob = self.build_sentence_and_iob(parts[0])
                if len(sentence_and_iob) > 0:
                    self.labeled_sentences.append(sentence_and_iob + ';' + parts[1])
                    counter += 1

    def generate_corpus(self, nb_sentences_to_generate: int):
        """
        Generate corpus
        :param nb_sentences_to_generate: number of sentences expected.
        """
        # Generate corpus
        self.logger.info('Generating corpus ...')

        # iterate over intents
        for intent in self.equalizer.intents:
            # select templates
            templates = self.templates_loader.get_templates_by_intents(intent)
            # calculate nb sentences are needed
            nb_sentences_needed = round(self.equalizer.intents[intent] * nb_sentences_to_generate / 100)
            self.generate_sentences(templates, nb_sentences_needed)

        self.logger.info('Generate {counter} sentences'.format(counter=len(self.labeled_sentences)))

        # shuffle
        self.logger.info('Shuffle corpus')
        random.shuffle(self.labeled_sentences)

    def save_corpus(self, output_path):
        """
        Save corpus in files
        :param output_path: output path directory
        """
        sentence_file = os.path.join(output_path, 'sentences.txt')
        iob_file = os.path.join(output_path, 'iobs.txt')
        intents_file = os.path.join(output_path, 'intents.txt')

        self.logger.info('Generate train outputs files : {sentence}, {iob} and {intents}'.format(
            sentence=sentence_file, iob=iob_file, intents=intents_file))

        with open(sentence_file, 'w') as f_sentence, open(iob_file, 'w') as f_iob, open(
                intents_file, 'w') as f_intent:
            for item in self.labeled_sentences:
                self.logger.debug("Process sentence : {}".format(item))
                parts = item.split(';')
                f_sentence.write(parts[0] + '\n')
                f_iob.write(parts[1] + '\n')
                f_intent.write(parts[2] + '\n')

    def get_generator(self):
        """
        :return: Return a python generator on the labeled sentences
        """
        for item in self.labeled_sentences:
            parts = item.split(';')
            if len(parts) > 3:
                print(item)
            yield parts[0], parts[1], parts[2]

    def get_labels_list(self):
        """
        Get all the iob labels used in the templates
        :return: List of iob labels
        """
        return self.dictionaries_loader.get_labels_list()

    def __init__(self, dictionaries_loader, templates_loader, equalizer):
        self.logger = logging.getLogger(__name__)

        self.dictionaries_loader = dictionaries_loader
        self.templates_loader = templates_loader
        self.equalizer = equalizer
