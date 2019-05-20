# -*- coding: gb2312 -*-
import pygame
import socket
import sys, os
import components.logger as logger
from pygame.locals import *

pygame.init()

PORT             = 50000
SERVER           = '127.0.0.1'  # In this case, localhost
PUBLIC_LOGGER    = logger.get_public_logger()
FPS              = 30
WIN_SIZE         = (1280, 720)  # Should be adjustable by "Setting"
WIDTH, HEIGHT    = WIN_SIZE
CLOCK            = pygame.time.Clock()
DISPLAY          = pygame.display.set_mode(WIN_SIZE)

BASIC_FONT_NORM  = pygame.font.Font('resources/MedievalSharp.ttf', 28)
BASIC_FONT_LARGE = pygame.font.Font('resources/MedievalSharp.ttf', 72)
BASIC_FONT_HUGE  = pygame.font.Font('resources/MedievalSharp.ttf', 180)
BASIC_FONT_ZH_NORM  = pygame.font.Font('resources/ZCOOLXiaoWei-Regular.ttf', 28)
BASIC_FONT_ZH_LARGE = pygame.font.Font('resources/ZCOOLXiaoWei-Regular.ttf', 72)
BASIC_FONT_ZH_HUGE  = pygame.font.Font('resources/ZCOOLXiaoWei-Regular.ttf', 180)




def main():
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
    terminate()


def menu():
    """
    Displays menu on DISPLAY Surface obj.
    :return 'play': User clicked the "Start Game" (开始游戏) button
    :return 'setting': User clicked the "Setting" (设置) button
    :return 'exit': User clicked the "Exit" (退出) button
    """
    bg_image        = image('resources/fake_background.png', resize=WIN_SIZE)
    bg_rect         = bg_image.get_rect()
    bg_rect.topleft = (0, 0)
    logo             = BASIC_FONT_ZH_HUGE.render("占卜大战", True, (0,0,0))
    logo_rect        = logo.get_rect()
    logo_rect.midtop = (WIDTH/2, HEIGHT*0.05)
    crystal_ball     = image('resources/fake_crystal_ball.png', resize=(HEIGHT/2, HEIGHT/1.78))
    ball_rect        = crystal_ball.get_rect()
    ball_rect.center = (WIDTH/2, HEIGHT-((HEIGHT-logo_rect.y-logo_rect.height)/2))
    #                   正中                   logo下方区域的中心

    start_button      = BASIC_FONT_ZH_NORM.render("开始游戏", True, (0,0,0))
    start_rect        = start_button.get_rect()
    start_rect.midtop = (WIDTH/2, ball_rect.y*1.4)
    while True:
        DISPLAY.blit(bg_image, bg_rect)
        DISPLAY.blit(crystal_ball, ball_rect)
        DISPLAY.blit(logo, logo_rect)
        DISPLAY.blit(start_button, start_rect)
        for event in pygame.event.get():  # Event loop
            if event.type == QUIT:
                terminate()
        pygame.display.flip()
        CLOCK.tick(FPS)
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
    try:
        if resize:
            resize = [int(x) for x in resize]
            surf = pygame.transform.scale(surf, resize)
        if flip:  # TODO: May have bugs please test
            if flip == "v":
                surf = pygame.transform.flip(surf, True, False)
            elif flip == "h":
                surf = pygame.transform.flip(surf, False, True)
            elif flip == "both":
                surf = pygame.transform.flip(surf, True, True)
        if spin:
            surf = pygame.transform.rotate(surf, spin)
    except Exception as e:
        PUBLIC_LOGGER.error('Unexpected exception when processing image file {img}: {ex}'.
                            format(img=path, ex=e))
    return surf


def terminate():
    logger.exit()
    sys.exit()


if __name__ == '__main__':
    main()
