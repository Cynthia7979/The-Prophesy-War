import pygame
import sys, os
import re
import textwrap
from . import logger
from math import ceil
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
CARD_DIMENSION   = (CARD_WIDTH, CARD_HEIGHT)

CLOCK            = pygame.time.Clock()
DISPLAY          = pygame.display.set_mode(WIN_SIZE)

BLACK = (0  , 0  , 0  )
WHITE = (255, 255, 255)

INT_FONT = {'en': 'resources/MedievalSharp.ttf',
            'zh': 'resources/ZCOOLXiaoWei-Regular.ttf'}
EN = 'en'
ZH = 'zh'
LANG = get_settings('language')
TINY  = ceil(15 * WIDTH/1080)
SMALL = ceil(28 * WIDTH/1080)
MEDIUM = ceil(40 * WIDTH/1080)
LARGE = ceil(72 * WIDTH/1080)
HUGE = ceil(180 * WIDTH/1080)
BASIC_FONT_NORM  = pygame.font.Font(INT_FONT['en'], SMALL)
BASIC_FONT_LARGE = pygame.font.Font(INT_FONT['en'], LARGE)
BASIC_FONT_HUGE  = pygame.font.Font(INT_FONT['en'], HUGE)
BASIC_FONT_ZH_NORM  = pygame.font.Font(INT_FONT['zh'], SMALL)
BASIC_FONT_ZH_LARGE = pygame.font.Font(INT_FONT['zh'], LARGE)
BASIC_FONT_ZH_HUGE  = pygame.font.Font(INT_FONT['zh'], HUGE)

PUBLIC_LOGGER = logger.get_public_logger('global_variable')


font_cache = {}


def font(size: int, lang=LANG):
    """
    Returns the indicated sized font.
    :param size: Size of the font.
    :param lang: Language of the font. Can be 'en' or 'zh'.
    :return: pygame.font.Font object.
    """
    if len(font_cache) >= 50:
        del font_cache[list(font_cache.keys())[-1]]
    try:
        f = font_cache[(size, lang)]
        PUBLIC_LOGGER.debug(f'Font of lang: {lang}, size: {size} found in cache')
        return f
    except KeyError:
        f = pygame.font.Font(INT_FONT[lang], size)
        font_cache[(size, lang)] = f
        PUBLIC_LOGGER.debug(f'Font of lang: {lang}, size: {size} created and cached')
        return f


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


def styled_text(raw, font_size):
    """
    Styled-text unwrapper.

    Styled-text looks like this:
        $000000$black text`$FFFFFF$white text

    If a segment has no style ($colorcode$) then it is interpreted as black (000000)
    :param raw: Raw text, as shown
    :param font_size: Size of text
    :return: pygame.Surface instance
    """
    split = raw.split('`')
    renders = []
    texts = []
    for s in split:
        try:
            hexcode = re.search('\$(.*)\$', s).group(1)
            rgbcode = tuple(int(hexcode[i:i + 2], 16) for i in (0, 2, 4))
        except (AttributeError, ValueError):
            rgbcode = BLACK
        text = s[s.rfind('$')+1:]
        renders.append(font(font_size).render(text, True, rgbcode))
        texts.append(text)
        PUBLIC_LOGGER.debug(f'Segment of styled text (color={rgbcode}, text={text}) rendered.')
    surf = pygame.Surface(font(font_size).render(''.join(texts), True, BLACK).get_rect().size, pygame.SRCALPHA)
    current_x = 0
    for r in renders:
        text_rect = r.get_rect()
        text_rect.topleft = (current_x, 0)
        surf.blit(r, text_rect)
        current_x = text_rect.right
        PUBLIC_LOGGER.debug(f'Segment of styled text blit to surface, x={current_x}')
    PUBLIC_LOGGER.debug(f"Styled text '{raw}' returned")
    return surf.copy()


def global_quit():
    pygame.font.quit()
    pygame.quit()
    logger.exit()
    sys.exit()
