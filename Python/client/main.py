# -*- coding: gb2312 -*-
import pygame
import socket
import sys, os
import components.scenes as scenes
import components.logger as logger
import components.json_editor as json
from components.global_variable import *
from pygame.locals import *

pygame.init()


def main():
    pygame.display.set_icon(image('resources/icon_placeholder.png'))
    pygame.display.set_caption('Prophesy War a0.1')
    while True:
        action = scenes.main_menu.main()
        if action == 'play':
            scenes.interval.zoom_ball()
            room = scenes.select_room.main()
            if room:
                pass
            scenes.interval.shrink_ball()
        elif action == 'setting':
            setting()
        elif action == 'exit':
            break
    terminate()


def setting():
    pass


def game(sock):
    pass


def terminate():
    logger.exit()
    sys.exit()


if __name__ == '__main__':
    main()
