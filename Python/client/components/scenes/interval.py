from ..logger import get_public_logger
from ..global_variable import *

"""
Intervals between scenes.
"""

SCENE_LOGGER = get_public_logger('interval')
CRYSTAL_BALL = 'resources/fake_crystal_ball.png'
BACKGROUND = 'resources/fake_background.png'
DURATION = FPS


def zoom_ball(start=(HEIGHT / 2, HEIGHT / 1.78),
              end=(HEIGHT / 2 * 1.8, HEIGHT / 1.78 * 1.8),
              start_pos=(WIDTH / 2, HEIGHT * 0.65),
              end_pos=(WIDTH / 2, HEIGHT / 2),
              duration=DURATION):
    SCENE_LOGGER.info('Scaling ball...')
    original_ball = image(CRYSTAL_BALL, resize=start)
    original_rect = original_ball.get_rect()
    original_rect.center = start_pos
    bg = image(BACKGROUND, resize=WIN_SIZE)
    bg_rect = bg.get_rect()
    bg_rect.topleft = (0, 0)
    DISPLAY.blit(original_ball, original_rect)
    DISPLAY.blit(bg, bg_rect)
    pygame.display.flip()
    (current_w, current_h), (current_x, current_y) = start, start_pos
    for i in range(int(duration/2)):
        DISPLAY.blit(bg, bg_rect)
        current_w += ceil((end[0] - start[0]) / duration)*2
        current_h += ceil((end[1] - start[1]) / duration)*2
        current_x += ceil((end_pos[0] - start_pos[0]) / duration)*2
        current_y += ceil((end_pos[1] - start_pos[1]) / duration)*2
        scaled_ball = pygame.transform.scale(original_ball, (int(current_w), int(current_h)))
        scaled_rect = scaled_ball.get_rect()
        scaled_rect.center = (current_x, current_y)
        DISPLAY.blit(scaled_ball, scaled_rect)
        pygame.display.flip()
        CLOCK.tick(FPS)
    DISPLAY.blit(bg, bg_rect)
    scaled_ball = image(CRYSTAL_BALL, resize=end)
    scaled_rect = scaled_ball.get_rect()
    scaled_rect.center = end_pos
    DISPLAY.blit(scaled_ball, scaled_rect)
    pygame.display.flip()
    return


def shrink_ball(start=(HEIGHT / 2 * 1.8, HEIGHT / 1.78 * 1.8),
                end=(HEIGHT / 2, HEIGHT / 1.78),
                start_pos=(WIDTH / 2, HEIGHT / 2),
                end_pos=(WIDTH / 2, HEIGHT * 0.65),
                duration=DURATION/2):
    return zoom_ball(start, end, start_pos, end_pos, duration)
