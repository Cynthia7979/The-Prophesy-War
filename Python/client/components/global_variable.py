import pygame
import sys, os
from math import ceil
from components.logger import get_public_logger
from .json_editor import get_settings

if os.path.basename(os.getcwd()) == 'components':
    os.chdir('../')
pygame.font.init()

PORT             = 50000
SERVER           = '127.0.0.1'  # In this case, localhost
FPS              = 30
WIN_SIZE         = tuple(get_settings(key='resolution'))
WIDTH, HEIGHT    = WIN_SIZE
CARD_WIDTH       = WIDTH/5
CARD_HEIGHT      = HEIGHT/2

CLOCK            = pygame.time.Clock()
DISPLAY          = pygame.display.set_mode(WIN_SIZE)

BLACK = (0, 0, 0)

INT_FONT = {'en': 'resources/MedievalSharp.ttf',
            'zh': 'resources/ZCOOLXiaoWei-Regular.ttf'}
EN = 'en'
ZH = 'zh'
LANG = get_settings('language')
SMALL = ceil(28 * WIDTH/1080)
LARGE = ceil(72 * WIDTH/1080)
HUGE = ceil(180 * WIDTH/1080)
BASIC_FONT_NORM  = pygame.font.Font(INT_FONT['en'], SMALL)
BASIC_FONT_LARGE = pygame.font.Font(INT_FONT['en'], LARGE)
BASIC_FONT_HUGE  = pygame.font.Font(INT_FONT['en'], HUGE)
BASIC_FONT_ZH_NORM  = pygame.font.Font(INT_FONT['zh'], SMALL)
BASIC_FONT_ZH_LARGE = pygame.font.Font(INT_FONT['zh'], LARGE)
BASIC_FONT_ZH_HUGE  = pygame.font.Font(INT_FONT['zh'], HUGE)

PUBLIC_LOGGER = get_public_logger('global_variable')


def font(size: int, lang=LANG):
    """
    Returns the indicated sized font.
    :param size: Size of the font.
    :param lang: Language of the font. Can be 'en' or 'zh'.
    :return: pygame.font.Font object.
    """
    PUBLIC_LOGGER.debug(f'Returning font of lang: {lang}, size: {size}')
    return pygame.font.Font(INT_FONT[lang], size)


def image(path, resize=None, flip=None, spin=None):
    """
    Loads an image file smartly. Works in resize -> flip -> spin order.
    :param path: String, image source
    :param resize: Tuple, resizes the image to (width, height). Default None.
    :param flip: Either "v", "h", or "both", flips the image in the corresponding way.
                 Default None.
    :param spin: Integer between 0 and 360, spins the image to `spin` degrees
    :return: pygame.Surface object
    """
    surf = pygame.image.load(path)
    PUBLIC_LOGGER.debug(f'Image loaded: {path}')
    try:
        if resize:
            resize = [int(x) for x in resize]
            surf = pygame.transform.scale(surf, resize)
            PUBLIC_LOGGER.debug(f'Image resized to {resize}')
        if flip:
            if flip == "v":
                surf = pygame.transform.flip(surf, True, False)
                PUBLIC_LOGGER.debug('Image flipped vertically')
            elif flip == "h":
                surf = pygame.transform.flip(surf, False, True)
                PUBLIC_LOGGER.debug('Image flipped horizontally')
            elif flip == "both":
                surf = pygame.transform.flip(surf, True, True)
                PUBLIC_LOGGER.debug('Image flipped both vertically and horizontally')
        if spin:
            surf = pygame.transform.rotate(surf, spin)
            PUBLIC_LOGGER.debug(f'Image spin to {spin} degrees')
    except Exception as e:
        PUBLIC_LOGGER.error(f'Unexpected exception when processing image file {path}: {e}')
    return surf
