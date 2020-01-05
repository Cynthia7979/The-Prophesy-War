"""
Global variables (note that file name is "global_variable")

Currently, this file is copied entirely from client.
"""
import pygame
import sys, os
from math import ceil
import re
#if os.path.basename(os.getcwd()) == 'client':
    #os.chdir('components/')
from . import logger


pygame.font.init()

# Socket
SERVER_PORT            = 50000
SERVER_HOST            = '127.0.0.1'  # In this case, localhost
ROOM_PORT              = 51000


# Colors R    G    B
BLACK = (0  , 0  , 0  )
WHITE = (255, 255, 255)
GREY  = (127, 127, 127)

PUBLIC_LOGGER = logger.get_public_logger('global_variable')  # Logger of global_variable and its funcs


font_cache = {}  # To prevent repetition


def strip_styled_text(text):
    """
    Resolving styled text for external modules
    :param text: Styled text
    :return: `dict` {'text':hexcode}
    """
    result = {}
    split = text.split('`')
    for segment in split:
        try:
            hexcode = re.search('\$(.*)\$', segment).group(1)  # Try to find the HEX $colorcode$
        except (AttributeError, ValueError):
            hexcode = '000000'  # If there is no style, then it is interpreted as black (000000)
        text = segment[segment.rfind('$') + 1:]  # Segment after colorcode. "$FF0000$This part"
        result[text] = hexcode
    return result


def global_quit():
    """
    Terminates all other things before program quits.
    Please update this function when you add something that needs extra quitting.
    :return: None
    """
    pygame.font.quit()
    pygame.quit()
    logger.exit()
    sys.exit()
