# -*- coding: gb2312 -*-
import pygame
import logger
import socket
import sys, os

PORT             = 50000
SERVER           = '127.0.0.1'  # In this case, localhost
PUBLIC_LOGGER    = logger.get_public_logger()
FPS              = 30
WIN_SIZE         = (1280, 720)  # Should be adjustable by "Setting"
WIDTH, HEIGHT    = (0, 1)       # Syntax sugar
BASIC_FONT       = pygame.font.Font('resources/MedievalSharp.ttf')

current_win_size = WIN_SIZE


def main():
    global CLOCK, DISPLAY
    pygame.init()
    CLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode(current_win_size)
    pygame.display.set_icon(image('resources/icon_placeholder.png'))
    pygame.display.set_caption('Prophesy War a0.1')
    while True:
        action = menu()
        if action == 'play':
            pass
        elif action == 'setting':
            setting()
        elif action == 'exit':
            break
    logger.exit()
    sys.exit()


def menu():
    """
    Displays menu on DISPLAY Surface obj.
    :return 'play': User clicked the "Start Game" (开始游戏) button
    :return 'setting': User clicked the "Setting" (设置) button
    :return 'exit': User clicked the "Exit" (退出) button
    Pseudo code:

    while True:
        display.display(background, createRoomButton, joinRoomButton, settingButton, exitButton)
        if clicked(createRoomButton):
            return 'create'
        elif clicked(joinRoomButton):
            return 'join'
        elif clicked(settingButton):
            return 'setting'
        elif clicked(exitButton):
            return 'exit'
        update(display)
    """
    bg_image = image('resources/fake_background.png', resize=current_win_size)
    bg_rect = pygame.Rect(bg_image.get_rect())
    crystal_ball = image('resources/fake_crystal_ball.png')
    logo = image('resources/fake_logo.png')
    while True:

    return ""


def setting():
    pass


def game(sock):
    pass


def connect():
    sock = socket.socket()
    sock.connect(SERVER)


def receive_game_data(sock):
    pass


def image(path, resize=None, flip=None, spin=None, surf=None):
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
    try:
        if resize:
            pygame.transform.scale(surf, resize, DestSurface=surf)
        if flip:  # TODO: May have bugs please test
            if flip == "v":
                surf = pygame.transform.flip(surf, True, False)
            elif flip == "h":
                surf = pygame.transform.flip(surf, False, True)
            elif flip == "both":
                surf = pygame.transform.flip(surf, True, True)
        if spin:
            surf = pygame.transform.rotate(suf, spin)
    except Exception as e:
        PUBLIC_LOGGER.error('Unexpected exception when processing image file {img}: {ex}'.
                            format(img=path, ex=e))
    return surf



if __name__ == '__main__':
    main()
