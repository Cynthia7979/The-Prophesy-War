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


