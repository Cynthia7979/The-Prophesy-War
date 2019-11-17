# -*- coding: gb2312 -*-
import sys, os
from ..global_variable import *
from .. import logger
from ..room import Room
from pygame.locals import *

SCENE_LOGGER = logger.get_public_logger('select_room')
room_page = 1


def main():
    """
    Displays select room scene on components.global_variable.DISPLAY.
    """
    SCENE_LOGGER.info('On select room')
    bg_image        = image('resources/fake_background.png', resize=WIN_SIZE)
    bg_rect         = bg_image.get_rect()
    bg_rect.topleft = (0, 0)

    create             = font(LARGE-2).render("创建房间", True, BLACK)
    create_rect        = create.get_rect()
    create_rect.midtop = (WIDTH/2, HEIGHT*0.05)

    crystal_ball     = image('resources/fake_crystal_ball.png', resize=(HEIGHT/2*1.8, HEIGHT/1.78*1.8))
    ball_rect        = crystal_ball.get_rect()
    ball_rect.center = (WIDTH/2, HEIGHT/2)

    l_arrow_image = image('resources/l_arrow.png')
    l_arrow_rect = l_arrow_image.get_rect()
    l_arrow_rect.midtop = ((WIDTH/2)+l_arrow_rect.width*2, HEIGHT/12 * 8.9)

    r_arrow_image = image('resources/r_arrow.png')
    r_arrow_rect = r_arrow_image.get_rect()
    r_arrow_rect.midtop = ((WIDTH/2)-r_arrow_rect.width*2, HEIGHT/12 * 8.9)

    #                                        "1"
    page_surface = font(SMALL).render(str(room_page), True, BLACK)
    page_rect = page_surface.get_rect()
    page_rect.midtop = (WIDTH/2,(HEIGHT / 12 * 9.125))

    rooms = []
    for i in range(7):  # 下面这一段6行等真有list以后替换掉
        roomname = "房间" + str(i+1)
        current_player = ()
        maxplayer = i
        playing = False
        #                                                                        address
        rooms.append(Room(roomname, i, maxplayer, current_player, playing, ('127.0.0.1', 50000)))

    for i in range(len(rooms)):
        current_room = rooms[i]
        # 把7个框放到该放的位置
        room_surf = current_room.get_state_surf()
        room_rect = room_surf.get_rect()
        room_rect.midtop = (WIDTH/2, (HEIGHT / 12*(2.2+i)))
        current_room.set_rect(room_rect)

    while True:
        DISPLAY.blit(bg_image, bg_rect)
        DISPLAY.blit(crystal_ball, ball_rect)
        DISPLAY.blit(create, create_rect)
        for i in range(len(rooms)):  # FIXME: Should be only 7
            DISPLAY.blit(rooms[i].surf, rooms[i].rect)
        DISPLAY.blit(l_arrow_image, l_arrow_rect)
        DISPLAY.blit(r_arrow_image, r_arrow_rect)
        DISPLAY.blit(page_surface, page_rect)

        for event in pygame.event.get():  # Event loop
            if event.type == QUIT:
                pygame.event.post(event)
                terminate()
            elif event.type == MOUSEBUTTONUP:
                if l_arrow_rect.collidepoint(event.pos):
                    SCENE_LOGGER.info('Arrow left')
                elif r_arrow_rect.collidepoint(event.pos):
                    SCENE_LOGGER.info('Arrow right')
                elif create_rect.collidepoint(event.pos):
                    SCENE_LOGGER.info('Create room')
                elif not ball_rect.collidepoint(event.pos):
                    SCENE_LOGGER.info('Background clicked, returning to main menu')
                    return None
                for i in range(len(rooms)):
                    if rooms[i].rect.collidepoint(event.pos):
                        chosen_room = rooms[i]
                        SCENE_LOGGER.debug(f'Room chosen: {chosen_room.room_id}')
                        if chosen_room.max_players == len(chosen_room.current_players):
                            pass  # TODO
                        elif chosen_room.max_players < len(chosen_room.current_players):
                            raise ValueError('Max player cannot be less then current players')
                        else:
                            return chosen_room.room_id

        pygame.display.flip()
        CLOCK.tick(FPS)


def terminate():
    logger.quit()
    sys.exit()


if __name__ == '__main__':
    main()
