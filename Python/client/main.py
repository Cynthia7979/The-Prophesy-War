# -*- coding: gb2312 -*-
import pygame
import sys, os
from components import scenes
from components import logger
from components.global_variable import image, global_quit
from pygame.locals import *


GLOBAL_LOGGER = logger.get_public_logger()  # Logger for main process


def main():
    """
    Holy main() of the client!
    """
    GLOBAL_LOGGER.info('Game started!')
    pygame.display.set_icon(image('resources/icon_placeholder.png'))
    pygame.display.set_caption('Prophesy War a0.1')
    load()
    while True:
        action = scenes.main_menu.main()  # Returns which button the player clicked.
        if action == 'play':
            scenes.interval.zoom_ball()
            room = scenes.select_room.main()
            if room:  # Chose a room
                #scenes.lobby.main(room)  # Lobby (where people can talk and view each other)
                scenes.game.main(room)  # pass room
                # scenes.game_over.main()  (isn't finished yet)
            else:  # Clicked the background
                scenes.interval.shrink_ball()
        elif action == 'setting':
            scenes.setting.load()
            scenes.interval.zoom_ball()
            scenes.setting.main()
            scenes.interval.shrink_ball()
        elif action == 'exit':
            break
    terminate()


def load():
    """
    Load all resources at the same time. Currently does nothing.
    """
    pass


def terminate():
    """
    Ending all progress.
    """
    global_quit()


if __name__ == '__main__':
    main()
