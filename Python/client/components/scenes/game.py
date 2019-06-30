# -*-coding: gb2312 -*-
import pygame
import sys, os
from ..global_variable import *
from .. import logger
from .. import hand
from pygame.locals import *


GLOBAL_LOGGER = logger.get_public_logger('game')
SIDEBAR_WIDTH = WIDTH/6
board_pos = (WIDTH/2, HEIGHT*-0.5)
sidebar = False


def main():
    dummy_card = hand.Card('', '', 1, [], '', '', '')
    dummy_hand = hand.Hand((dummy_card,)*10)

    bg_surf = image('resources/fake_background.png', resize=(WIDTH, HEIGHT))
    bg_rect = bg_surf.get_rect()
    bg_rect.topleft = (0, 0)
    board_surf = image('resources/fake_board.png', resize=(HEIGHT*2, HEIGHT*2))
    while True:
        DISPLAY.blit(bg_surf, bg_rect)
        show_gameboard(board_surf)
        show_hand(dummy_hand)
        for event in pygame.event.get():  # Event loop
            if event.type == QUIT:
                pygame.event.post(event)
                terminate()
        pygame.display.flip()
        CLOCK.tick(FPS)


def show_gameboard(board_surf):
    board_rect = board_surf.get_rect()
    board_rect.center = board_pos
    DISPLAY.blit(board_surf, board_rect)


def show_hand(h: hand.Hand):
    hand_disp = []
    margin = (WIDTH-SIDEBAR_WIDTH-CARD_WIDTH/2)/len(h.get_cards()) if sidebar else (WIDTH-CARD_WIDTH/2)/len(h.get_cards())
    current_x = 0
    for c in h.get_cards():
        rect = c.image.get_rect()
        rect.bottomleft = (current_x, HEIGHT+CARD_HEIGHT/4)
        hand_disp.append((c.image, rect))
        current_x += margin-1
    for i, r, in hand_disp:
        DISPLAY.blit(i, r)


def terminate():
    # room.exit()
    logger.exit()
    sys.exit()
