# -*-coding: gb2312 -*-
import pygame
import sys, os
from ..global_variable import *
from ..hand import *
from ..card import *
from ..mission import Mission
from .. import logger
from pygame import Surface
from pygame.locals import *



SCENE_LOGGER = logger.get_public_logger('game')
BOARD_WIDTH, BOARD_HEIGHT = HEIGHT*2, HEIGHT*2
SIDEBAR_WIDTH, SIDEBAR_HEIGHT = (WIDTH/4, HEIGHT*1.1)
SIDEBAR_RECT = pygame.Rect(0,0,SIDEBAR_WIDTH, SIDEBAR_HEIGHT)
SIDEBAR_RECT.midright = (WIDTH, HEIGHT / 2)

SIDEBAR_IMAGE = image('resources/fake_sidebar.png', resize=(SIDEBAR_WIDTH, SIDEBAR_HEIGHT))
SIDEBAR_HIDE_IMAGE = image('resources/fake_sidebar_hide.png', resize=(WIDTH / 50, HEIGHT / 4))  # The arrow


def main(room):
    """
    Shows and plays the game.
    Client won't process any calculation. Only the host server processes the game.
    """
    SCENE_LOGGER.info(f'Game started at room_placeholder')  # TODO
    dragging_board = False  # Is the player dragging the board?
    mouse_pos_cache = None  # Last mouse (x, y), used to calculate x and y offsets
    board_center_pos = (WIDTH / 2, HEIGHT * -0.5)  # Initial center of the circular board
    board_scale = 1.0  # Initial enlarge/shrink scale
    sidebar = True  # Is the side bar being displayed?
    real_width = WIDTH - (SIDEBAR_WIDTH * sidebar)  # Width available for everything except the sidebar

    # The following things are for creating placeholders
    dummy_background = image('resources/background.png', resize=(CARD_WIDTH, CARD_HEIGHT))
    dummy_card = ItemCard('', 1, 10, '', '', '', dummy_background)
    dummy_hand = Hand((dummy_card,)*10)
    dummy_mission = Mission('$999999$黑夜是否嚎叫？`$EEEEEE$仅在月亏之时', 1)

    dummy_prophesy_button = font(SMALL).render("进行占卜", True, BLACK) #占卜 button试做
    dummy_prophesy_button_rect = dummy_prophesy_button.get_rect()

    bg_surf = image('resources/fake_background.png', resize=(WIDTH, HEIGHT))  # Game background
    bg_rect = bg_surf.get_rect()
    bg_rect.topleft = (0, 0)
    board_surf = image('resources/fake_board.png', resize=(HEIGHT*2, HEIGHT*2))  # Game board
    while True:
        mouse_pos = pygame.mouse.get_pos()
        DISPLAY.blit(bg_surf, bg_rect)

        show_gameboard(board_surf, board_center_pos, board_scale)  # show gameboard on screen
        show_hand(dummy_hand, real_width)  # show hand cards on screen
        show_sidebar(sidebar, [dummy_mission]*10, 0, [])  # show sidebar on screen
        show_prophesy_button(dummy_prophesy_button,dummy_prophesy_button_rect)

        if dragging_board:
            board_center_pos = get_new_board_center_pos(mouse_pos, mouse_pos_cache, board_center_pos)
            mouse_pos_cache = mouse_pos
        for event in pygame.event.get():  # Event loop
            if event.type == QUIT:
                pygame.event.post(event)  # QUIT event is needed by other parts of the program
                terminate()
            elif event.type == MOUSEBUTTONDOWN:
                # TODO
                # if clicked_on_something:
                #    do something
                # elif clicked_on_another_thing:
                #    do something
                # else:
                dragging_board = True
                mouse_pos_cache = event.pos

                # “进行占卜按键”事件
                if dummy_prophesy_button_rect.collidepoint(mouse_pos_cache):
                    DISPLAY.blit(dummy_prophesy_button, (0,0))
                    SCENE_LOGGER.info(f'START PROPHESY')
                    # show_prophesy_selection( )

            elif event.type == MOUSEBUTTONUP:
                if event.button == 4:  # Mouse wheel rolled up
                    if board_scale + 0.1 > 2.9:  # If it is big enough. 2.9 (not 3) to prevent float type bugs
                        board_scale = 2.9
                    else:
                        board_scale += 0.1
                elif event.button == 5:  # Mouse wheel rolled down
                    if board_scale - 0.1 <= 0:
                        board_scale = 0.1
                    else:
                        board_scale -= 0.1
                if dragging_board:  # User released mouse
                    # Final pos
                    board_center_pos = get_new_board_center_pos(event.pos, mouse_pos_cache, board_center_pos)
                    # Stop dragging board
                    dragging_board = False
                else:
                    pass  # TODO: Other things
                # elif event.type ==

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
    :param aval_width: Available width for hand display. If sidebar is shown, it will be WIDTH-sidebar.
    If not then WIDTH
    :return: None
    """
    y = HEIGHT * 1.1  # This is *mid-bottom y*. The lower side of the card will be below the window
    avl_width = aval_width - CARD_WIDTH/2 - 10  # Leave right margin (probably)
    overlap = CARD_WIDTH - avl_width / len(h.get_cards())  # How much a card will overlap onto another card
    current_x = 10
    for c in h.get_cards():
        x = current_x + CARD_WIDTH - overlap
        rect = c.image.get_rect()
        rect.midbottom = (x, y)
        DISPLAY.blit(c.image, rect)
        current_x = x


def play_card(card: Card):
    """
    Displays the play card animation
    :param card: Which card to play
    """
    screen = DISPLAY.copy()  # Animation will be displayed on top of the original GUI
    screen.convert_alpha()  # Make it transparent!
    black_mask = pygame.Surface((WIDTH, HEIGHT), flags=SRCALPHA)
    black_mask.fill((0, 0, 0, 200))
    screen.blit(black_mask, (0, 0))
    y = HEIGHT / 2
    x = 0
    SCENE_LOGGER.debug(f'Doing play_card animation for {card.name}')
    for i in range(1, FPS+5):  # The whole animation will be a bit longer than a second
        DISPLAY.blit(screen, (0, 0))
        # 这里用中文解释一下
        # x是t的（类似于？）二次函数。t可以被看成是（已经完成动画的百分比）-50
        # 当t小于0，图象开口朝下；当t等于-50（最小值）时，x等于0（窗口最左边）
        # 当t大于0，图象开口朝上；当t等于50（最大值）时，x等于WIDTH（窗口最右边）
        # 当t等于0，也就是动画刚好进行到一半时，x等于1/2 WIDTH（窗口正中央）
        # 最终效果就是卡片由左到中间速度由快到慢（飞入），在中间静止一帧，然后由中间到右速度由慢到快（飞出）
        # 具体计算见下面
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
        # Sidebar background
        DISPLAY.blit(SIDEBAR_IMAGE, SIDEBAR_RECT)
        # Leftmost x-coord of the sidebar
        sidebar_left = (WIDTH-SIDEBAR_WIDTH)*1.05

        # Missions
        # Display mission title
        mission_title_surf = font(SMALL).render('任务', True, BLACK)
        mission_title_rect = mission_title_surf.get_rect()
        mission_title_rect.topleft = (sidebar_left, 10)
        DISPLAY.blit(mission_title_surf, mission_title_rect)

        mission_slice = missions[mission_page:mission_page+4]
        current_y = mission_title_rect.bottom*1.3   # Below mission title
        for n, m in enumerate(mission_slice):  # index, item
            start_of_a_mission = True
            mod_m_description = strip_styled_text(m.description)  # Modified mission description {pureText: textStyle}
            current_text = []
            current_styled_text = []
            for segment, segment_color in mod_m_description.items():
                if start_of_a_mission:
                    number = 2 * mission_page + 1 + n  # E.g. Page=0, Index=1(count from 0), 2*0+1+1=2
                    current_text.append(f'{number}. {segment}')                            # '1. text'
                    current_styled_text.append(f'{number}. `${segment_color}${segment}')  # '1. `$ffff00$text'
                    start_of_a_mission = False
                else:  # Already in the middle of rendering a mission
                    styled = f'  `${segment_color}${segment}'  # Indent: '  `$ffff00$text'
                    current_text.append(segment)
                    if len(''.join(current_text)) > 14:  # if text is too long
                        cache = current_text.pop()  # Temporarily store this piece of text
                        # Display what we have now
                        text_surf = styled_text(''.join(current_styled_text), TINY)
                        text_rect = text_surf.get_rect()
                        text_rect.topleft = (sidebar_left, current_y)
                        DISPLAY.blit(text_surf, text_rect)
                        # And start a new line
                        current_y = text_rect.bottom + 5  # 5 pixels below last line
                        current_text = [cache]
                        current_styled_text = [styled]
                    else:  # else just add new text to this line
                        current_styled_text.append(styled)
            if current_styled_text:  # Almost the end of a mission, display what's left
                text_surf = styled_text(''.join(current_styled_text), TINY)
                text_rect = text_surf.get_rect()
                text_rect.topleft = (sidebar_left, current_y)
                DISPLAY.blit(text_surf, text_rect)
                current_y = text_rect.bottom + 5
            current_y += 5  # extra 5 pixels margin after a mission
            # End of a mission

        # TODO:Chat




    else:
        # Shows only the arrow
        sidebar_rect = SIDEBAR_HIDE_IMAGE.get_rect()
        sidebar_rect.midright = (WIDTH, HEIGHT/2)
        DISPLAY.blit(SIDEBAR_HIDE_IMAGE, sidebar_rect)


def is_drag_board(pos, board_center_pos, board_surf, side_bar):
    """
    Is the current pos of mouse on gameboard
    :param pos: Pos of mouse
    :param board_center_pos: Center of gameboard
    :param board_surf: Surface of gameboard
    :param side_bar: Is the sidebar displayed or hidden?
    :return: Boolean value.
    """
    if side_bar and SIDEBAR_RECT.collidepoint(pos[0], pos[1]):  # If user didn't click the board, but the sidebar
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
    # Equivalent to (new_pos[0]-old_pos[0], new_pos[1]-old_pos[1])
    pos_alter = tuple([new_pos[x]-old_pos[x] for x in (0,1)])
    return tuple([board_center_pos[x] + pos_alter[x] for x in (0,1)])


def show_prophesy_button(b: Surface, r: Rect): # place prophesy button a little above hands
    DISPLAY.blit(b, r)


def show_prophesy_selection(b: Surface, r: Rect):  #

    # dummy_prophesy_button = font(SMALL).render("进行占卜", True, BLACK) #占卜 button试做
    # dummy_prophesy_button_rect = dummy_prophesy_button.get_rect()

    # send a message to server: I want do a prophesy
    # server send back result
    # show result on screen and adjust data
    a = 0

    # DISPLAY.blit(b,r)


def terminate():
    SCENE_LOGGER.warning(f'Force leaving room room_placeholder')  # TODO
    # room.exit() (TODO)
    global_quit()
    sys.exit()
