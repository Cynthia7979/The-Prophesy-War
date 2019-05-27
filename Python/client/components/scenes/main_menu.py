import pygame
import sys, os
from .. import logger
from pygame.locals import *
from ..global_variable import *


LOGGER = logger.get_public_logger('main_menu')


def main():
    """
    Displays main on DISPLAY Surface obj.
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
    #                     正中                  logo下方区域的中心

    start_button      = BASIC_FONT_ZH_NORM.render("开始游戏", True, (0,0,0))
    start_rect        = start_button.get_rect()
    start_rect.midtop = (WIDTH/2, ball_rect.y*1.4)
    setting_button      = BASIC_FONT_ZH_NORM.render('设置', True, (0,0,0))
    setting_rect        = setting_button.get_rect()
    setting_rect.midtop = (WIDTH/2, start_rect.y+start_rect.height+ball_rect.y*0.15)
    exit_button      = BASIC_FONT_ZH_NORM.render('退出', True, (0, 0, 0))
    exit_rect        = setting_button.get_rect()
    exit_rect.midtop = (WIDTH / 2, setting_rect.y + setting_rect.height + ball_rect.y * 0.15)
    while True:
        DISPLAY.blit(bg_image, bg_rect)
        DISPLAY.blit(crystal_ball, ball_rect)
        DISPLAY.blit(logo, logo_rect)
        DISPLAY.blit(start_button, start_rect)
        DISPLAY.blit(setting_button, setting_rect)
        DISPLAY.blit(exit_button, exit_rect)
        for event in pygame.event.get():  # Event loop
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONUP:
                if start_rect.collidepoint(event.pos):
                    return 'play'
                elif setting_rect.collidepoint(event.pos):
                    return 'setting'
                elif exit_rect.collidepoint(event.pos):
                    return 'exit'
        pygame.display.flip()
        CLOCK.tick(FPS)


def terminate():
    logger.exit()
    sys.exit()

