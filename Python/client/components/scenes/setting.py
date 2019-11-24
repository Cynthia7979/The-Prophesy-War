"""
The settings (aka preference) scene.

**Structure:**

column: A page of settings (entries)


"""
# -*- coding: gb2312 -*-
from .. import logger
from .. import json_editor
from ..global_variable import *
from pygame.locals import *

SCENE_LOGGER = logger.get_public_logger('setting')


def main():
    SCENE_LOGGER.info('On setting.')
    current_column = 0  # Start from the first page
    while True:
        display_parts()
#         Selection        Column   - If user clicked inside these rectangles, then they clicked these things
        sel_rectangles, col_rectangles = display_selections(current_column)
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONUP:
                x, y = event.pos
                for rect in sel_rectangles.keys():
                    rect = pygame.Rect(rect)  # Convert tuple to Rect
                    if rect.collidepoint(x, y):  # If user clicked one of the selection rectangles
                        settings = json_editor.get_settings()  # Get current settings
                        key, choices, selection = sel_rectangles[tuple(rect)]  # Infos of the entry which was clicked
                        next_selection = tuple(choices.items())[(selection+3) % (len(choices.keys()))][1]  # ??????
                        settings[key] = next_selection
                        SCENE_LOGGER.debug(f'Clicked on {key}, switched to {next_selection}')
                        json_editor.update_settings(settings)
                for rect in col_rectangles.keys():
                    rect = pygame.Rect(rect)
                    if rect.collidepoint(x, y):  # If user clicked one of the column titles
                        current_column += 1
                        current_column %= max_column
                        # The display of swiching column will be done in the next iteration
                        SCENE_LOGGER.debug(f'Switched to column {current_column}')
        CLOCK.tick(FPS)
        pygame.display.flip()


def load():
    """
    Load all resources that is used in setting scene.
    Might be removed, because they are already loaded in global_variables.
    :return:
    """
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
    """
    Displays the background and widgets.
    """
    DISPLAY.blit(bg_image, bg_rect)
    DISPLAY.blit(crystal_ball, ball_rect)
    DISPLAY.blit(separator, separator_rect)


def display_selections(col):
    """
    Displays the entries of the current column and returns necessary info.
    :param col: Current column number
    :return: :var settings_rectangles(0) and :var column_rectangles(1).
    * :var column_rectangles: Rectangles to check if the user switched column. Dictionary of {columnRect: tupleID}
    * :var settings_rectangles: Rectangles to check if the user clicked on any of the entries. Dictionary of
    {entryRect: (entryID(in English, used to edit settings.json), possibleChoices, indexOfCurrentSelection)}.
      * `possibleChoices`: dictionary of {choiceName: choiceValue(to set in settings.json)}
    """
    current_x = separator_rect.x * 1.2
    column_rectangles = {}
    for column in setlist.keys():
        if tuple(setlist.keys()).index(column) == col:  # Shadow the column title if it is selected
            text = shadowed_text(column, SMALL)
            rect = text.get_rect()
            rect.bottomleft = (current_x, separator_rect.y*0.95)
            DISPLAY.blit(text, rect)
        else:
            text = font(SMALL).render(column, True, BLACK)
            rect = text.get_rect()
            rect.bottomleft = (current_x, separator_rect.y * 0.95)
            DISPLAY.blit(text, rect)
        column_rectangles[tuple(rect)] = tuple(setlist.keys()).index(column)
        current_x += separator_rect.w / len(tuple(setlist.keys()))  # Move right

    current_x = separator_rect.x * 1.2
    current_y = separator_rect.y * 1.5
    selected_col = tuple(setlist.values())[col]  # Get entries of selected column
    settings_rectangles = {}
    for label, v in selected_col.items():
        correspondent = v[0]  # English entry ID to use in settings.json
        choices = v[1]  # Possible choices

        # Display name of setting
        text = font(SMALL).render(label+':', True, BLACK)
        rect = text.get_rect()
        rect.topleft = (current_x, current_y)
        DISPLAY.blit(text, rect)
        current_y += HEIGHT / 15

        # Display current selection
        inv_col = {list_to_tuple(v): k for k, v in choices.items()}  # Inverse of dictionary column
        selection_index = tuple(inv_col.keys()).index(list_to_tuple(json_editor.get_settings(key=correspondent)))
        # Index (among all possible choices) of current selection
        current_selection = tuple(inv_col.values())[selection_index]
        sel_text = shadowed_text(current_selection, SMALL)
        sel_rect = sel_text.get_rect()
        sel_rect.midleft = (rect.midright[0]+7, rect.midright[1]+1)
        settings_rectangles[tuple(sel_rect)] = (correspondent, choices, selection_index)
        DISPLAY.blit(sel_text, sel_rect)
    return settings_rectangles, column_rectangles


def list_to_tuple(l):
    """
    Convert something that is *possibly* a list to a tuple.
    :param l: Something that might be a list.
    :return: Something that is most likely a tuple.
    """
    if type(l) == list:
        return tuple(l)
    else:
        return l


def terminate():
    global_quit()
