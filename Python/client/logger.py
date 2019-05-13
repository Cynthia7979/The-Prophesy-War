import logging
from time import strftime
from shutil import move

default_level = logging.DEBUG


def get_public_logger(name='client', loglevel='debug'):
    logger = logging.getLogger(name)
    strlevel = {'debug': logging.DEBUG,
                'info': logging.INFO,
                'warning': logging.WARNING,
                'error': logging.ERROR,
                'critical': logging.CRITICAL}
    try:
        logger.setLevel(strlevel[loglevel])
    except KeyError:
        public_logger.warning('Logger "{name}" did not provide an available log level.'.format(name=name))
        logger.setLevel(default_level)
    logger.addHandler(default_fh)
    logger.addHandler(default_ch)
    return logger


def logged_class(cls):
    class_name = cls.__name__
    logger = logging.getLogger('P2P.'+class_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(default_fh)
    logger.propagate = False
    logger.debug('Logger {} created.'.format(class_name))
    setattr(cls, 'logger', logger)
    return cls


def move_log():
    default_fh.close()
    try:
        move('prophesy_war.log', strftime('Logs/log_%y-%m-%d_%H-%M-%S.log'))
    except OSError as e:
        # As when multiple launchers were opened at the same time
        if e.winerror == 32:
            public_logger.warning("Another program is using log file. Now exiting.")
        else:
            public_logger.error("Unexpected error when moving log file: {}".format(e))


default_ch = logging.StreamHandler().setLevel(logging.DEBUG)
default_fh = logging.FileHandler('prophesy_war_client.log').setLevel(default_level)
public_logger = get_public_logger('global')
