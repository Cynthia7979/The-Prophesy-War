# -*-coding: gb2312 -*-
import pygame
import sys, os
import textwrap
from ..global_variable import *
from ..hand import *
from ..card import *
from ..mission import Mission
from .. import logger
from pygame.locals import *


GLOBAL_LOGGER = logger.get_public_logger('game')
SIDEBAR_WIDTH = WIDTH/4
SIDEBAR_HEIGHT = HEIGHT*1.1
board_center_pos = (WIDTH / 2, HEIGHT * -0.5)
sidebar = True
real_width = WIDTH - (SIDEBAR_WIDTH * sidebar)
sidebar_image = image('resources/fake_sidebar.png', resize=(SIDEBAR_WIDTH, SIDEBAR_HEIGHT))
sidebar_hide_image = image('resources/fake_sidebar_hide.png', resize=(WIDTH/50, HEIGHT/4))


def main():
    dummy_card = Card('', '', 1, [], '', '', '')
    dummy_hand = Hand((dummy_card,)*10)
    dummy_mission = Mission('$8B0000$Dr. Bright`遗失了他的`$999999$682专用报纸筒', 1)

    bg_surf = image('resources/fake_background.png', resize=(WIDTH, HEIGHT))
    bg_rect = bg_surf.get_rect()
    bg_rect.topleft = (0, 0)
    board_surf = image('resources/fake_board.png', resize=(HEIGHT*2, HEIGHT*2))
    while True:
        DISPLAY.blit(bg_surf, bg_rect)
        show_gameboard(board_surf)
        show_hand(dummy_hand)
        show_sidebar([dummy_mission]*10, 0, [])
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
        GLOBAL_LOGGER.debug(f'Playing card "{card.get_name()}", pos={(x, y)}')
        DISPLAY.blit(card.image, card_rect)
        CLOCK.tick(FPS)
        pygame.display.flip()


def show_sidebar(missions, mission_page, chat_history):
    if sidebar:
        sidebar_rect = sidebar_image.get_rect()
        sidebar_rect.midright = (WIDTH, HEIGHT/2)
        DISPLAY.blit(sidebar_image, sidebar_rect)

        # Missions
        SIDEBAR_LEFT = (WIDTH-SIDEBAR_WIDTH)*1.05
        mission_title_surf = font(SMALL).render('任务', True, BLACK)
        mission_title_rect = mission_title_surf.get_rect()
        mission_title_rect.topleft = (SIDEBAR_LEFT, 10)
        DISPLAY.blit(mission_title_surf, mission_title_rect)

        mission_slice = missions[mission_page:mission_page+4]
        current_y = mission_title_rect.bottom*1.3
        for n, m in enumerate(mission_slice):
            start_of_a_mission = True
            for s in textwrap.wrap(m.description, 14):  # It cuts off styled text, FIXME
                if start_of_a_mission:
                    s = f'{2 * mission_page + 1 + n}. `{s}'
                    start_of_a_mission = not start_of_a_mission
                else:
                    s = f'  `{s}'
                text_surf = styled_text(s, TINY)
                text_rect = text_surf.get_rect()
                text_rect.topleft = (SIDEBAR_LEFT, current_y)
                DISPLAY.blit(text_surf, text_rect)
                current_y = text_rect.bottom + 5
            current_y += 5



    else:
        sidebar_rect = sidebar_hide_image.get_rect()
        sidebar_rect.midright = (WIDTH, HEIGHT/2)
        DISPLAY.blit(sidebar_hide_image, sidebar_rect)




def terminate():
    GLOBAL_LOGGER.warning(f'Force leaving room room_placeholder')  # TODO
    # room.exit()
    global_quit()
    sys.exit()
