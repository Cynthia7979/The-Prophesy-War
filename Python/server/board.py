from .human import Player, NPC
import pygame

# Screen dimensions and coordinates
ORIGIN = (0, 0)
# You may adjust these values as you'd like, depending on your screen resolution
WIDTH = 800  # 1024
HEIGHT = 600  # 768
FONT_HEIGHT = 30                       # The height of the text display.


class Board(object):
    def __init__(self):
        self.clients = []
        self.regions = []

    def start_game(self):
        # main loop
        while self.running:
            # event handling, gets all event from the event queue
            self.event_loop()

    def event_loop(self):

            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    self.running = False


