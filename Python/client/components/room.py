import pygame
from .global_variable import *


class Room(object):

    """
    Attributes:
        room_name (str): The name of the room.
        current_players (int): Current number of players.
        max_players (int): Max player.
        playing (bool): Playing or waiting.
    """

    def __init__(self, room_name: str, room_id: int, max_players: int, current_players=0, playing=False):
        """
        Initializes a Room object.
        :param room_name: Room name.
        :param current_players: Current # of player(s).
        :param max_players: Max # of players.
        :param playing: Is the room in game or waiting to start.
        """
        self.room_name      = room_name
        self.room_id        = room_id
        self.current_players = current_players
        self.max_players     = max_players
        self.playing        = playing
        self.surf = self.get_state_surf()
        self.rect = self.surf.get_rect()

    def set_state(self, room_name: str=None, max_players: int=None, current_players: int=None, playing: bool=None):
        """
        Set (updates) the state of a room.
        :param room_name: Room name.
        :param current_players: Current # of player (s)
        :param max_players: Max # of players.
        :param playing: Is the room in game or waiting to start.
        """
        if room_name: self.room_name = room_name
        if current_players: self.current_players = current_players
        if max_players: self.max_players = max_players
        if playing:   self.playing = playing

    def get_state_surf(self) -> pygame.Surface:
        if self.playing:
            p = "【游戏中】"
        else:
            p = "【等待中】"
        return font(SMALL).render(
            "{name}              {state} {player}/{max}".format(name=self.room_name,
                                                                state=p,
                                                                player=self.current_players,
                                                                max=self.max_players), True, BLACK)

    def set_rect(self, rect):
        self.rect = rect
