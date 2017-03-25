import re
import string

SLOT_REGEX = re.compile('\(.*\)')  # ("\\(.*\\|.*\\)")


def standardization(item: str) -> str:

    # remove '\n'
    item = item.strip('\n')
    # remove(bla bla)
    item = re.sub(SLOT_REGEX, '', item)
    # strip punctuation
    item = item.translate(string.punctuation)

    return item
