import pygame


class Room(object):

    """
    Attributes:
        room_name (str): The name of the room.
        current_player (int): Current number of players.
        max_player (int): Max player.
        playing (bool): Playing or waiting.
    """

    rect: pygame.rect
    surface: pygame.Surface
    state_line: pygame.Surface # 选择页面出现的那行字

    def __init__(self, r_n:str, c_p:int, m_p:int,p: bool, s: pygame.Surface):
        self.room_name = r_n
        self.current_player = c_p
        self.max_player = m_p
        self.playing = p
        self.surface = s

        self.rect = self.surface.get_rect()

    def set_state(self, r_n:str, c_p:int, m_p:int,p: bool):
        self.room_name = r_n
        self.current_player = c_p
        self.max_player = m_p
        self.playing = p

    def get_state_line(self) -> str:
        if self.playing:
            p = "【游戏中】"
        else:
            p = "【等待中】"
        return self.room_name + "              " + p + str(self.current_player) + "/" + str(self.max_player)