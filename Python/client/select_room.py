# -*- coding: gb2312 -*-
import pygame
import socket
import sys, os
import components.logger as logger
import components.json_editor as json
from pygame.locals import *

from room import Room

pygame.init()

PORT             = 50000
SERVER           = '127.0.0.1'  # In this case, localhost
PUBLIC_LOGGER    = logger.get_public_logger()
FPS              = 30
WIN_SIZE         = (1080, 720)  # TODO: Should be adjustable by "Setting"
WIDTH, HEIGHT    = WIN_SIZE
CLOCK            = pygame.time.Clock()
DISPLAY          = pygame.display.set_mode(WIN_SIZE)

BASIC_FONT_NORM  = pygame.font.Font('resources/MedievalSharp.ttf', 28)
BASIC_FONT_LARGE = pygame.font.Font('resources/MedievalSharp.ttf', 72)
BASIC_FONT_HUGE  = pygame.font.Font('resources/MedievalSharp.ttf', 180)
BASIC_FONT_ZH_NORM  = pygame.font.Font('resources/ZCOOLXiaoWei-Regular.ttf', 28)
BASIC_FONT_ZH_LARGE = pygame.font.Font('resources/ZCOOLXiaoWei-Regular.ttf', 72)
BASIC_FONT_ZH_HUGE  = pygame.font.Font('resources/ZCOOLXiaoWei-Regular.ttf', 180)
#  TODO: Should also be adjustable


current_surface = 'menu'
rooms = [Room]
room_page = 1

def main():


    pygame.display.set_icon(image('resources/icon_placeholder.png'))
    pygame.display.set_caption('Prophesy War a0.1')
    while True:
        action = menu()
        print(action)
        if action == 'play':
            pass
        elif action == 'setting':
            setting()
        elif action == 'exit':
            break
    terminate()


def menu() -> str:
    """
    Displays menu on DISPLAY Surface obj.
    :return 'play': User clicked the "Start Game" (开始游戏) button
    :return 'setting': User clicked the "Setting" (设置) button
    :return 'exit': User clicked the "Exit" (退出) button
    """
    bg_image        = image('resources/fake_background.png', resize=WIN_SIZE)
    bg_rect         = bg_image.get_rect()
    bg_rect.topleft = (0, 0)
    logo             = BASIC_FONT_ZH_LARGE.render("创建房间", True, (0,0,0))
    logo_rect        = logo.get_rect()

    logo_rect.midtop = (WIDTH/2, HEIGHT*0.05)
    crystal_ball     = image('resources/fake_crystal_ball.png', resize=(HEIGHT/2*1.8 , HEIGHT/1.78*1.8))
    ball_rect        = crystal_ball.get_rect()
    ball_rect.center = (WIDTH/2, HEIGHT/2)

    l_arrow_image = image('resources/l_arrow.png')
    l_arrow_rect = l_arrow_image.get_rect()
    l_arrow_rect.topleft = ((WIDTH/2) + (WIDTH/20),HEIGHT/12 * 9)

    r_arrow_image = image('resources/r_arrow.png')
    r_arrow_rect = r_arrow_image.get_rect()
    r_arrow_rect.topleft = ((WIDTH/2)  - (WIDTH / 20*2), HEIGHT / 12 * 9)

    #                                                   "1"
    room_page_surface = BASIC_FONT_ZH_NORM.render(str(room_page), True, (0, 0, 0))
    room_page_surface_rect = room_page_surface.get_rect()
    room_page_surface_rect = (WIDTH/2,(HEIGHT / 12 * 9.125))

    rooms = []
    r_width = int(WIDTH/3)
    r_height = int(HEIGHT/16)

    for i in range(7):

        # 下面这一段6行等真有list以后替换掉
        roomname = "房间" + str(i+1)
        current_player = 0
        maxplayer = i
        playing = False
        surface = pygame.Surface((r_width,r_height),pygame.SRCALPHA, 32) #这行和下面这行是网上抄的，用来把背景变透明
        surface = surface.convert_alpha()

        rooms.append(Room(roomname,current_player,maxplayer,playing,surface))

    for i in range(len(rooms)):
        #把7个框放到该放的位置
        rooms[i].rect = rooms[i].surface.get_rect()
        rooms[i].rect.topleft = ((r_width, HEIGHT / 12 * (2 + i)))
        #如果需要的话，在框里放上一行字
        rooms[i].stateline      = BASIC_FONT_ZH_NORM.render(rooms[i].get_state_line(), True, (0, 0, 0))
        rooms[i].surface.blit(rooms[i].stateline,rooms[i].stateline.get_rect())


    while True:
        DISPLAY.blit(bg_image, bg_rect)
        DISPLAY.blit(crystal_ball, ball_rect)
        DISPLAY.blit(logo, logo_rect)

        for i in range(len(rooms)):
            DISPLAY.blit(rooms[i].surface, rooms[i].rect)

        DISPLAY.blit(l_arrow_image,l_arrow_rect)
        DISPLAY.blit(r_arrow_image,r_arrow_rect)
        DISPLAY.blit(room_page_surface, room_page_surface_rect)

        for event in pygame.event.get():  # Event loop
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONUP:
                if l_arrow_rect.collidepoint(event.pos):
                    return 'L'
                elif r_arrow_rect.collidepoint(event.pos):
                    return 'R'

                for i in range(len(rooms)):
                    if rooms[i].rect.collidepoint(event.pos):
                        return rooms[i].room_name
        pygame.display.flip()
        CLOCK.tick(FPS)


def setting():
    pass


def game(sock):
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