# -*-coding: gb2312 -*-
import pygame
import sys, os
from ..global_variable import *
from ..hand import *
from ..card import *
from ..mission import Mission
from .. import logger
from pygame.locals import *


SCENE_LOGGER = logger.get_public_logger('game')
BOARD_WIDTH, BOARD_HEIGHT = HEIGHT*2, HEIGHT*2
SIDEBAR_WIDTH, SIDEBAR_HEIGHT = (WIDTH/4, HEIGHT*1.1)
SIDEBAR_RECT = pygame.Rect(0,0,SIDEBAR_WIDTH, SIDEBAR_HEIGHT)
SIDEBAR_RECT.midright = (WIDTH, HEIGHT / 2)

SIDEBAR_IMAGE = image('resources/fake_sidebar.png', resize=(SIDEBAR_WIDTH, SIDEBAR_HEIGHT))
SIDEBAR_HIDE_IMAGE = image('resources/fake_sidebar_hide.png', resize=(WIDTH / 50, HEIGHT / 4))


def main(room):
    """
    Shows and plays the game.
    Client won't process any calculation. Only the host processes the game.
    :return: None
    """
    SCENE_LOGGER.info(f'Game started at room_placeholder')
    dragging_board = False
    mouse_pos_cache = None
    board_center_pos = (WIDTH / 2, HEIGHT * -0.5)
    board_scale = 1.0
    sidebar = True
    real_width = WIDTH - (SIDEBAR_WIDTH * sidebar)

    dummy_background = image('resources/background.png', resize=(CARD_WIDTH, CARD_HEIGHT))
    dummy_card = ItemCard('', '', 1, 10, '', '', '', dummy_background)
    dummy_hand = Hand((dummy_card,)*10)
    dummy_mission = Mission('$999999$黑夜是否嚎叫？`$EEEEEE$仅在月亏之时', 1)

    bg_surf = image('resources/fake_background.png', resize=(WIDTH, HEIGHT))
    bg_rect = bg_surf.get_rect()
    bg_rect.topleft = (0, 0)
    board_surf = image('resources/fake_board.png', resize=(HEIGHT*2, HEIGHT*2))
    while True:
        mouse_pos = pygame.mouse.get_pos()
        DISPLAY.blit(bg_surf, bg_rect)
        show_gameboard(board_surf, board_center_pos, board_scale)
        show_hand(dummy_hand, real_width)
        show_sidebar(sidebar, [dummy_mission]*10, 0, [])
        if dragging_board:
            board_center_pos = get_new_board_center_pos(mouse_pos, mouse_pos_cache, board_center_pos)
            mouse_pos_cache = mouse_pos
        for event in pygame.event.get():  # Event loop
            if event.type == QUIT:
                pygame.event.post(event)
                terminate()
            elif event.type == MOUSEBUTTONDOWN:
                # if clicked_on_something:
                #    do something
                # elif clicked_on_another_thing:
                #    do something
                # else:
                    dragging_board = True
                    mouse_pos_cache = event.pos
            elif event.type == MOUSEBUTTONUP:
                if event.button == 4:  # Mouse wheel rolled up
                    if board_scale+0.1 > 2.9:  # Prevent float bugs
                        board_scale = 2.9
                    else:
                        board_scale += 0.1
                elif event.button == 5:  # Mouse wheel rolled down
                    board_scale -= 0.1
                    if board_scale-0.1 <= 0:
                        board_scale = 0.1
                if dragging_board:
                    board_center_pos = get_new_board_center_pos(event.pos, mouse_pos_cache, board_center_pos)
                    dragging_board = False
                else:
                    pass  # Other things
        pygame.display.flip()
        CLOCK.tick(FPS)


def show_gameboard(board_surf, board_center_pos, board_scale):
    """
    Shows gameboard (The circle thing) for one frame
    :param board_surf: Surface to blit to
    :param board_center_pos: Center of the circle
    :param board_scale: How big (or small) is the board. E.g. 2 means 2x bigger
    :return: None
    """
    board_surf = pygame.transform.scale(board_surf, (int(BOARD_WIDTH*board_scale), int(BOARD_HEIGHT*board_scale)))
    board_rect = board_surf.get_rect()
    board_rect.center = board_center_pos
    DISPLAY.blit(board_surf, board_rect)


def show_hand(h: Hand, aval_width):
    """
    Shows cards in hand
    :param h: Hand
    :param aval_width: Available width for hand display. If sidebar is shown, it will be WIDTH-sidebar. If not then WIDTH
    :return: None
    """
    y = HEIGHT * 1.1
    avl_width = aval_width - CARD_WIDTH/2 - 10
    fold_width = CARD_WIDTH - avl_width / len(h.get_cards())
    current_x = 10
    for c in h.get_cards():
        x = current_x - fold_width + CARD_WIDTH
        rect = c.image.get_rect()
        rect.midbottom = (x, y)
        DISPLAY.blit(c.image, rect)
        current_x = x


def play_card(card: Card):
    """
    Displays the play card animation
    :param card: Which card to play
    :return: None
    """
    screen = DISPLAY.copy()
    screen.convert_alpha()
    black_mask = pygame.Surface((WIDTH, HEIGHT), flags=SRCALPHA)
    black_mask.fill((0, 0, 0, 200))
    screen.blit(black_mask, (0, 0))
    y = HEIGHT / 2
    x = 0
    SCENE_LOGGER.debug(f'Start playing card {card.name}')
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
        DISPLAY.blit(card.image, card_rect)
        CLOCK.tick(FPS)
        pygame.display.flip()


def show_sidebar(sidebar, missions, mission_page, chat_history):
    """
    Shows sidebar, including missions and chat
    :param sidebar: Is sidebar shown or not
    :param missions: Missions the player accepted
    :param mission_page: Current page of mission. E.g. 1 for the first page
    :param chat_history: Dict of {styled_username: what_they_say}
    :return: None
    """
    if sidebar:
        DISPLAY.blit(SIDEBAR_IMAGE, SIDEBAR_RECT)

        # Missions
        sidebar_left = (WIDTH-SIDEBAR_WIDTH)*1.05
        mission_title_surf = font(SMALL).render('任务', True, BLACK)
        mission_title_rect = mission_title_surf.get_rect()
        mission_title_rect.topleft = (sidebar_left, 10)
        DISPLAY.blit(mission_title_surf, mission_title_rect)
        mission_slice = missions[mission_page:mission_page+4]
        current_y = mission_title_rect.bottom*1.3
        for n, m in enumerate(mission_slice):
            start_of_a_mission = True
            mod_m_description = strip_styled_text(m.description)
            current_text = []
            current_styled_text = []
            for segment, segment_color in mod_m_description.items():
                if start_of_a_mission:
                    number = 2 * mission_page + 1 + n
                    styled = f'{number}. `${segment_color}${segment}'
                    current_text.append(f'{number}. {segment}')
                    current_styled_text.append(styled)
                    start_of_a_mission = False
                else:
                    styled = f'  `${segment_color}${segment}'
                    current_text.append(segment)
                    if len(''.join(current_text)) > 14:  # Text is too long
                        cache = current_text.pop()  # Temporarily store this piece of text
                        # Display what we have now
                        text_surf = styled_text(''.join(current_styled_text), TINY)
                        text_rect = text_surf.get_rect()
                        text_rect.topleft = (sidebar_left, current_y)
                        DISPLAY.blit(text_surf, text_rect)
                        # Start a new line
                        current_y = text_rect.bottom + 5
                        current_text = [cache]
                        current_styled_text = [styled]
                    else:
                        current_styled_text.append(styled)
            if current_styled_text:
                text_surf = styled_text(''.join(current_styled_text), TINY)
                text_rect = text_surf.get_rect()
                text_rect.topleft = (sidebar_left, current_y)
                DISPLAY.blit(text_surf, text_rect)
                current_y = text_rect.bottom + 5
            current_y += 5
            # End of a mission

        # Chat




    else:
        # Shows the arrow
        sidebar_rect = SIDEBAR_HIDE_IMAGE.get_rect()
        sidebar_rect.midright = (WIDTH, HEIGHT/2)
        DISPLAY.blit(SIDEBAR_HIDE_IMAGE, sidebar_rect)


def is_drag_board(pos, board_center_pos, board_surf, sidebar):
    """
    Is the current pos of mouse on gameboard
    :param pos: Pos of mouse
    :param board_center_pos: Center of gameboard
    :param board_surf: Surface of gameboard
    :return: Bool.
    """
    if sidebar and SIDEBAR_RECT.collidepoint(pos[0], pos[1]):
        return False
    board_rect = board_surf.get_rect()
    board_rect.center = board_center_pos
    return board_rect.collidepoint(pos)


def get_new_board_center_pos(new_pos, old_pos, board_center_pos):
    """
    Move the board by the movement of mouse pos
    :param new_pos: New mouse pos
    :param old_pos: Old mouse pos (preferably from the last frame)
    :param board_center_pos: Center of the gameboard
    :return: Tuple. New pos for the center of gameboard.
    """
    pos_alter = tuple([new_pos[x]-old_pos[x] for x in (0,1)])
    return tuple([board_center_pos[x] + pos_alter[x] for x in (0,1)])


def terminate():
    SCENE_LOGGER.warning(f'Force leaving room room_placeholder')  # TODO
    # room.exit()
    global_quit()
    sys.exit()
