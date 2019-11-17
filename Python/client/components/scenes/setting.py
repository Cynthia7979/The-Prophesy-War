"""
The settings (aka preference) scene.

**Structure:**

column: Big page of a group of entries.

"""
# -*- coding: gb2312 -*-
from .. import logger
from .. import json_editor
from ..global_variable import *
from pygame.locals import *

SCENE_LOGGER = logger.get_public_logger('setting')


def main():
    SCENE_LOGGER.info('On setting.')
    current_column = 0
    while True:
        display_parts()
        sel_rectangles, col_rectangles = display_selections(current_column)
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONUP:
                x, y = event.pos
                for rect in sel_rectangles.keys():
                    rect = pygame.Rect(rect)
                    if rect.collidepoint(x, y):
                        settings = json_editor.get_settings()
                        key, choices, selection = sel_rectangles[tuple(rect)]
                        next_selection = tuple(choices.items())[(selection+3) % (len(choices.keys()))][1]
                        settings[key] = next_selection
                        SCENE_LOGGER.debug(f'Clicked on {key}, switched to {next_selection}')
                        json_editor.update_settings(settings)
                for rect in col_rectangles.keys():
                    rect = pygame.Rect(rect)
                    if rect.collidepoint(x, y):
                        current_column += 1
                        current_column %= max_column
                        SCENE_LOGGER.debug(f'Switched to column {current_column}')
        pygame.display.flip()


def load():
    global crystal_ball, ball_rect, bg_image, bg_rect, separator, separator_rect, setlist, max_column
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
    max_column = len(setlist.keys())


def display_parts():
    DISPLAY.blit(bg_image, bg_rect)
    DISPLAY.blit(crystal_ball, ball_rect)
    DISPLAY.blit(separator, separator_rect)


def display_selections(col):
    current_x = separator_rect.x * 1.2
    column_rectangles = {}
    for column in setlist.keys():
        if tuple(setlist.keys()).index(column) == col:
            text = shadowed_text(column, SMALL)
            rect = text.get_rect()
            rect.bottomleft = (current_x, separator_rect.y*0.95)
            DISPLAY.blit(text, rect)
        else:
            text = font(SMALL).render(column, True, BLACK)
            rect = text.get_rect()
            rect.bottomleft = (current_x, separator_rect.y * 0.95)
            DISPLAY.blit(text, rect)
        column_rectangles[tuple(rect)] = tuple(setlist.keys()).index(column)  # index of currently displaying column
        current_x += separator_rect.w / len(tuple(setlist.keys()))

    current_x = separator_rect.x * 1.2
    current_y = separator_rect.y * 1.5
    selected_col = tuple(setlist.values())[col]
    settings_rectangles = {}  # For clicking events
    for label, v in selected_col.items():
        correspondent = v[0]
        choices = v[1]

        # Display name of setting
        text = font(SMALL).render(label+':', True, BLACK)
        rect = text.get_rect()
        rect.topleft = (current_x, current_y)
        DISPLAY.blit(text, rect)
        current_y += HEIGHT / 15

        # Display current selection

        inv_col = {list_to_tuple(v): k for k, v in choices.items()}
        selection_index = tuple(inv_col.keys()).index(list_to_tuple(json_editor.get_settings(key=correspondent)))
        current_selection = tuple(inv_col.values())[selection_index]
        sel_text = shadowed_text(current_selection, SMALL)
        sel_rect = sel_text.get_rect()
        sel_rect.midleft = (rect.midright[0]+7, rect.midright[1]+1)
        settings_rectangles[tuple(sel_rect)] = (correspondent, choices, selection_index)
        DISPLAY.blit(sel_text, sel_rect)
    return settings_rectangles, column_rectangles


def list_to_tuple(l):
    if type(l) == list:
        return tuple(l)
    else:
        return l


def terminate():
    global_quit()
