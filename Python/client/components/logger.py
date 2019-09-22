import logging
import sys, os
from time import strftime
from shutil import move

STRLEVEL = {'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL}

default_strlevel = 'debug'
default_level = STRLEVEL[default_strlevel]
default_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

default_ch = logging.StreamHandler()
default_fh = logging.FileHandler('prophesy_war_client.log')
default_ch.setLevel(logging.DEBUG)
default_fh.setLevel(default_level)
default_fh.setFormatter(default_formatter)
default_ch.setFormatter(default_formatter)


def get_public_logger(name='client', loglevel=default_strlevel):
    logger = logging.getLogger(name)

    try:
        logger.setLevel(STRLEVEL[loglevel])
    except KeyError:
        public_logger.warning('Logger "{name}" did not provide an available log level.'.format(name=name))
        logger.setLevel(default_level)
    logger.addHandler(default_fh)
    logger.addHandler(default_ch)
    return logger


def logged_class(cls):
    class_name = cls.__name__
    logger = logging.getLogger('PW.'+class_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(default_fh)
    logger.propagate = False
    logger.debug('Logger {} created.'.format(class_name))
    setattr(cls, 'logger', logger)
    return cls


def move_log():
    try:
        move('components/prophesy_war_client.log', strftime('Logs/log_%y-%m-%d_%H-%M-%S.log'))
    except OSError as e:
        if e.winerror == 32:  # As when multiple games were opened at the same time
            public_logger.warning("Another program is using log file. Now exiting.")
        else:
            public_logger.error("Unexpected error when moving log file: {}".format(e))


def exit():
    public_logger.info('Ready to close.')
    default_fh.close()
    default_ch.close()
    move_log()
    sys.exit()


public_logger = get_public_logger('logger')
