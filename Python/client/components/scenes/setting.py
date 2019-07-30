# -*- coding: gb2312 -*-
from .. import logger
from .. import json_editor
from ..global_variable import *
from pygame.locals import *

SCENE_LOGGER = logger.get_public_logger('setting')


def main():
    SCENE_LOGGER.info('On setting.')
    current_column = 0
    while True:  # Game loop
        display_parts()
        display_selections(current_column)
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
        pygame.display.flip()


def load():
    global crystal_ball, ball_rect, bg_image, bg_rect, separator, separator_rect, setlist
    crystal_ball     = image('resources/fake_crystal_ball.png', resize=(HEIGHT/2*1.8, HEIGHT/1.78*1.8))
    ball_rect        = crystal_ball.get_rect()
    ball_rect.center = (WIDTH/2, HEIGHT/2)
    bg_image        = image('resources/fake_background.png', resize=WIN_SIZE)
    bg_rect         = bg_image.get_rect()
    bg_rect.topleft = (0, 0)
    separator      = image('resources/separator.png', resize=(WIDTH/2, HEIGHT/500))
    separator_rect = separator.get_rect()
    separator_rect.center = (WIDTH/2, ball_rect.h/5+ball_rect.y)

    setlist = json_editor.get_settings_list()


def display_parts():
    DISPLAY.blit(bg_image, bg_rect)
    DISPLAY.blit(crystal_ball, ball_rect)
    DISPLAY.blit(separator, separator_rect)


def display_selections(col):
    current_x = separator_rect.x * 1.2
    for column in setlist.keys():
        text = font(SMALL).render(column, True, BLACK)
        rect = text.get_rect()
        rect.bottomleft = (current_x, separator_rect.y * 0.95)
        DISPLAY.blit(text, rect)
        current_x += separator_rect.w / len(list(setlist.keys()))

    current_x = separator_rect.x * 1.2
    current_y = separator_rect.y * 1.5
    selected_col = list(setlist.values())[col]
    for k, v in selected_col.items():
        correspondent = v[0]
        choices = v[1]
        text = font(SMALL).render(k+':', True, BLACK)
        rect = text.get_rect()
        rect.topleft = (current_x, current_y)
        DISPLAY.blit(text, rect)
        current_y += HEIGHT / 15


def terminate():
    global_quit()
