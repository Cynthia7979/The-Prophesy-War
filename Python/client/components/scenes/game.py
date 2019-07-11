# -*-coding: gb2312 -*-
import pygame
import sys, os
import time
from ..global_variable import *
from ..hand import *
from ..card import *
from .. import logger
from pygame.locals import *


GLOBAL_LOGGER = logger.get_public_logger('game')
SIDEBAR_WIDTH = WIDTH/6
board_center_pos = (WIDTH / 2, HEIGHT * -0.5)
sidebar = False
real_width = WIDTH - (SIDEBAR_WIDTH * sidebar)


def main():
    dummy_card = Card('', '', 1, [], '', '', '')
    dummy_hand = Hand((dummy_card,)*10)

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
    board_rect.center = board_center_pos
    DISPLAY.blit(board_surf, board_rect)


def show_hand(h: Hand):
    y = HEIGHT * 1.1
    avl_width = real_width - CARD_WIDTH/2 - 10
    fold_width = CARD_WIDTH - avl_width / len(h.get_cards())
    current_x = 10
    for c in h.get_cards():
        x = current_x - fold_width + CARD_WIDTH
        rect = c.image.get_rect()
        rect.midbottom = (x, y)
        DISPLAY.blit(c.image, rect)
        current_x = x


def play_card(card: Card):
    screen = DISPLAY.copy()
    screen.convert_alpha()
    black_mask = pygame.Surface((WIDTH, HEIGHT), flags=SRCALPHA)
    black_mask.fill((0, 0, 0, 200))
    screen.blit(black_mask, (0, 0))
    y = HEIGHT / 2
    x = 0
    GLOBAL_LOGGER.debug(f'Start playing card {card.get_name()}')
    for i in range(1, FPS+5):
        DISPLAY.blit(screen, (0, 0))
        t = i*3 - 50
        if t < 0:
            x = -(WIDTH/5000*t**2)+WIDTH/2
        else:
            x = WIDTH/5000*t**2+WIDTH/2
        for event in pygame.event.get():  # Event loop
            if event.type == QUIT:
                pygame.event.post(event)
                terminate()
        card_rect = card.image.get_rect()
        card_rect.center = (x, y)
        GLOBAL_LOGGER.debug(f'Playing card "{card.get_name}", pos={(x, y)}')
        DISPLAY.blit(card.image, card_rect)
        CLOCK.tick(FPS)
        pygame.display.flip()


def terminate():
    GLOBAL_LOGGER.warning(f'Force leaving room room_placeholder')  # TODO
    # room.exit()
    logger.exit()
    sys.exit()