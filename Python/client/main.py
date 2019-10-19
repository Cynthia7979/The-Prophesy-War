# -*- coding: gb2312 -*-
import pygame
import sys, os
from components import scenes
from components import logger
from components.global_variable import *
from pygame.locals import *


GLOBAL_LOGGER = logger.get_public_logger()


def main():
    GLOBAL_LOGGER.info('Game started!')
    pygame.display.set_icon(image('resources/icon_placeholder.png'))  # global_variable
    pygame.display.set_caption('Prophesy War a0.1')
    load()
    while True:
        action = scenes.main_menu.main()
        if action == 'play':
            scenes.interval.zoom_ball()
            room = scenes.select_room.main()
            if room:
                scenes.lobby.main(room)
                scenes.game.main(room)  # pass room
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
    pass


def terminate():
    global_quit()  # global_variable


if __name__ == '__main__':
    main()
