# -*- coding: gb2312 -*-
import pygame
import sys, os
from ..global_variable import *
from .. import logger
from ..room import Room
from pygame.locals import *

PUBLIC_LOGGER = logger.get_public_logger('select_room')

rooms = [Room]
room_page = 1


def main():
    """
    Displays select room scene on components.global_variable.DISPLAY.
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
        surface = pygame.Surface((r_width, r_height), pygame.SRCALPHA, 32)  # 这行和下面这行是网上抄的，用来把背景变透明
        surface = surface.convert_alpha(surface)

        rooms.append(Room(roomname, current_player, maxplayer, playing, surface))

    for i in range(len(rooms)):
        # 把7个框放到该放的位置
        rooms[i].rect = rooms[i].surface.get_rect()
        rooms[i].rect.topleft = ((r_width, HEIGHT / 12 * (2 + i)))
        # 如果需要的话，在框里放上一行字
        rooms[i].stateline      = BASIC_FONT_ZH_NORM.render(rooms[i].get_state_line(), True, (0, 0, 0))
        rooms[i].surface.blit(rooms[i].stateline, rooms[i].stateline.get_rect())

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
                pygame.event.post(event)
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


def terminate():
    logger.exit()
    sys.exit()


if __name__ == '__main__':
    main()
