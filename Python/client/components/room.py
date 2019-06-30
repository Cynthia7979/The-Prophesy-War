import pygame
from .global_variable import *


class Room(object):

    """
    Attributes:
        room_name (str): The name of the room.
        current_player (int): Current number of players.
        max_player (int): Max player.
        playing (bool): Playing or waiting.
    """

    def __init__(self, r_n: str, r_id: int, c_p: int, m_p: int, p: bool):
        """
        Initializes a Room object.
        :param r_n: Room name.
        :param c_p: Current # of player(s).
        :param m_p: Max # of players.
        :param p: Is the room in game or waiting to start.
        """
        self.room_name      = r_n
        self.room_id        = r_id
        self.current_player = c_p
        self.max_player     = m_p
        self.playing        = p
        self.surf = self.get_state_surf()
        self.rect = self.surf.get_rect()

    def set_state(self, r_n: str=None, c_p: int=None, m_p: int=None, p: bool=None):
        """
        Set (updates) the state of a room.
        :param r_n: Room name.
        :param c_p: Current # of player (s)
        :param m_p: Max # of players.
        :param p: Is the room in game or waiting to start.
        """
        if r_n: self.room_name = r_n
        if c_p: self.current_player = c_p
        if m_p: self.max_player = m_p
        if p:   self.playing = p

    def get_state_surf(self) -> pygame.Surface:
        if self.playing:
            p = "【游戏中】"
        else:
            p = "【等待中】"
        return font(SMALL).render(
            "{name}              {state} {player}/{max}".format(name=self.room_name,
                                                                state=p,
                                                                player=self.current_player,
                                                                max=self.max_player), True, BLACK)

    def set_rect(self, rect):
        self.rect = rect
