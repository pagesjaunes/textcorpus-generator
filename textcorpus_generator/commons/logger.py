import logging
from logging.handlers import RotatingFileHandler

# Application logger
logger = logging.getLogger()

# Logger conf
def configure(p_level, p_dir=None, p_filename=None, p_max_filesize=100000, p_max_files=1, p_prefix=None):

    # default value
    logger.setLevel(logging.DEBUG)

    # String format
    if p_prefix:
        formatter = logging.Formatter('[' + p_prefix + '] %(asctime)s :: %(levelname)s :: %(module)s.%(funcName)s : %(message)s')
    else:
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(module)s.%(funcName)s : %(message)s')

    # Handler console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(p_level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if p_dir is not None:
        # File handler
        file_path = p_dir + '/' + p_filename
        file_handler = RotatingFileHandler(file_path, 'a', p_max_filesize, p_max_files)
        file_handler.setLevel(p_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
