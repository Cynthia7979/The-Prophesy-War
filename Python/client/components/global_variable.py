"""
Global variables (note that file name is "global_variable")
"""
import pygame
import sys, os
from math import ceil
import re
#if os.path.basename(os.getcwd()) == 'client':
    #os.chdir('components/')
from . import logger
from .json_editor import get_settings


pygame.font.init()

# Socket
PORT             = 50000
SERVER           = '127.0.0.1'  # In this case, localhost

# Pygame
FPS              = 30  # Be careful changing this because it is associated with some animation speed...
WIN_SIZE         = tuple(get_settings(key='resolution'))
WIDTH, HEIGHT    = WIN_SIZE
CLOCK            = pygame.time.Clock()
DISPLAY          = pygame.display.set_mode(WIN_SIZE)  # The window

# Card
CARD_WIDTH       = WIDTH/5
CARD_HEIGHT      = HEIGHT/2
CARD_DIMENSION   = (CARD_WIDTH, CARD_HEIGHT)

# Colors R    G    B
BLACK = (0  , 0  , 0  )
WHITE = (255, 255, 255)
GREY  = (127, 127, 127)

# Bilingual
EN = 'en'
ZH = 'zh'
LANG = get_settings('language')

# Fonts
INT_FONT = {'en': 'resources/MedievalSharp.ttf',
            'zh': 'resources/ZCOOLXiaoWei-Regular.ttf'}
TINY   = ceil(15 * WIDTH/1080)
SMALL  = ceil(28 * WIDTH/1080)
MEDIUM = ceil(40 * WIDTH/1080)
LARGE  = ceil(72 * WIDTH/1080)
HUGE   = ceil(180 * WIDTH/1080)
BASIC_FONT_NORM  = pygame.font.Font(INT_FONT['en'], SMALL)
BASIC_FONT_LARGE = pygame.font.Font(INT_FONT['en'], LARGE)
BASIC_FONT_HUGE  = pygame.font.Font(INT_FONT['en'], HUGE)
BASIC_FONT_ZH_NORM  = pygame.font.Font(INT_FONT['zh'], SMALL)
BASIC_FONT_ZH_LARGE = pygame.font.Font(INT_FONT['zh'], LARGE)
BASIC_FONT_ZH_HUGE  = pygame.font.Font(INT_FONT['zh'], HUGE)

PUBLIC_LOGGER = logger.get_public_logger('global_variable')  # Logger of global_variable and its funcs


font_cache = {}  # To prevent repetition


def font(size: int, lang=LANG):
    """
    Returns the specified sized font.
    :param size: Size of the font.
    :param lang: Language of the font. Can be either 'en' or 'zh'.
    :return: pygame.font.Font object.
    """
    if len(font_cache) >= 50:
        del font_cache[list(font_cache.keys())[-1]]
    try:
        f = font_cache[(size, lang)]
    except KeyError:
        try:
            f = pygame.font.Font(INT_FONT[lang], size)
        except KeyError:
            raise ValueError(f'"lang" should be either "zh" or "en", not "{lang}"')
        font_cache[(size, lang)] = f
        PUBLIC_LOGGER.debug(f'Font of lang: {lang}, size: {size} created and cached')
    return f


def image(path, resize=None, flip=None, spin=None):
    """
    Loads an image file smartly. Works in resize -> flip -> spin order.
    :param path: Image source. `string`.
    :param resize: Resize the image to `(width, height)`. `tuple`. Default `None`.
    :param flip: Either "v", "h", or "both", flips the image in the corresponding way.
                 Default `None`.
    :param spin: Integer between 0 and 360, spins the image to `spin` degrees
    :return: `pygame.Surface` instance
    """
    surf = pygame.image.load(path)
    try:
        if resize:
            resize = [int(x) for x in resize]
            surf = pygame.transform.scale(surf, resize)
        if flip:
            if flip == "v":
                surf = pygame.transform.flip(surf, True, False)
            elif flip == "h":
                surf = pygame.transform.flip(surf, False, True)
            elif flip == "both":
                surf = pygame.transform.flip(surf, True, True)
        if spin:
            surf = pygame.transform.rotate(surf, spin)
    except Exception as e:
        PUBLIC_LOGGER.error(f'Unexpected exception when processing image file {path}: {e}')
    PUBLIC_LOGGER.debug(f'Image loaded: {path}')
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
    split = raw.split('`')  # Separate segments of different colors
    renders = []  # All rendered texts (pygame.Surface)
    texts = []  # All raw texts (string) used for calculating length
    for s in split:
        try:
            hexcode = re.search('\$(.*)\$', s).group(1)  # Try to find the HEX $colorcode$
            rgbcode = tuple(int(hexcode[i:i + 2], 16) for i in (0, 2, 4))  # And transmit it into RGB
        except (AttributeError, ValueError):
            rgbcode = BLACK  # If there is no style, then it is interpreted as black (000000)
        text = s[s.rfind('$')+1:]  # Segment after colorcode. "$FF0000$This part"
        renders.append(font(font_size).render(text, True, rgbcode))
        texts.append(text)
    # Add all texts together
    # Create the surface to draw on
    surf = pygame.Surface(font(font_size).render(''.join(texts), True, BLACK).get_rect().size, pygame.SRCALPHA)
    current_x = 0
    for r in renders:
        text_rect = r.get_rect()
        text_rect.topleft = (current_x, 0)  # Specify where the text really is
        surf.blit(r, text_rect)  # Draw the text onto the surface
        current_x = text_rect.right  # Specify where the next piece of text should be
    #PUBLIC_LOGGER.debug(f"Styled text '{raw}' returned")  # Too noisy
    return surf.copy()


def shadowed_text(text, size, color=BLACK, shadow_color=GREY):
    """
    Makes shadowed text
    :param text: Raw text
    :param size: Size of the texr
    :param color: Color of the text. Default black.
    :param shadow_color: Color of the shadow. Default `GREY`.
    :return: `pygame.Surface`
    """
    shadow = font(size).render(text, True, shadow_color)
    text = font(size).render(text, True, color)
    text_rect = text.get_rect()
    text_rect.topleft = (-2, -2)  # Shadow offset
    shadow.blit(text, text_rect)  # Put text onto shadow
    return shadow


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
