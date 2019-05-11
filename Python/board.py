
from card import Card, ItemCard, RitualCard

from human import Player, NPC
import pygame

# Screen dimensions and coordinates
ORIGIN = (0, 0)
# You may adjust these values as you'd like, depending on your screen resolution
WIDTH = 800  # 1024
HEIGHT = 600  # 768
FONT_HEIGHT = 30                       # The height of the text display.

class Board:

    running: bool #whether this board is running or not
    screen: pygame.Surface
    subscreen: [pygame.Surface]

    _player_array: [Player]
    _npc_array: [NPC]
    _deck_array: [Card]
    _item_deck_array: [ItemCard]
    _ritual_deck_array: [RitualCard]
    _discard_deck_array: [Card]
    #_event_array: [Event]

    _current_player: Player


    def __init__(self):

        self.running = True

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SCP-CN-505 - The Prophcesy War 0.0a")


        self.start_game()

    def start_game(self):

        self.event_loop()

    def event_loop(self):
        # main loop
        while self.running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    self.running = False



