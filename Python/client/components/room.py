import pygame
from .global_variable import *


class Room(object):
    def __init__(self, room_name: str, room_id: int, max_players: int, address: str,
                 current_players={}, playing=False):
        """
        Initializes a Room object.
        :param room_name: Room name.
        :param current_players: Dict of {ip: playername}
        :param max_players: Max # of players.
        :param address: IP of the host client, string.
        :param current_players: Any preexisting players when creating the Room instance.
        :param playing: Is the room in game or waiting to start.
        """

        self.room_name       = room_name
        self.room_id         = room_id
        self.current_players = current_players
        self.max_players     = max_players
        self.playing         = playing
        self.address = address
        self.surf = self.get_state_surf()  # Check client/components/scenes/select_room.py  TODO better implementation
        self.rect = self.surf.get_rect()

    def set_state(self, room_name: str = None, max_players: int = None,
                  playing: bool = None):
        """
        Set (updates) the state of a room.

        *Parameters*: Check __init__()
        """
        if room_name: self.room_name = room_name
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
                                                                player=len(self.current_players),
                                                                max=self.max_players), True, BLACK)

    def set_rect(self, rect):
        self.rect = rect

    def add_player(self, player_name: str, player_ip: str, player_color:tuple):
        self.current_players[player_ip] = (player_name, player_color)

    def __gt__(self, other):
        if isinstance(other, Room):
            if self.room_id > other.room_id:
                return True
            else:
                return False
        else:
            raise TypeError('Room instance cannot be compared with non-Room instances.')

    def __eq__(self, other):
        if not (self > other or self < other):
            return True
        else:
            return False

    def __ge__(self, other):
        if self > other or self == other:
            return True
        else:
            return False

    def __ne__(self, other):
        if not self == other:
            return True
        else:
            return False

    def __repr__(self):
        return str((self.room_name, self.room_id, self.max_players, self.address, self.current_players, self.playing))


def unfold(r):
    r = r.strip('\\')
    if type(r) == str:
        r = eval(r)
    else: raise TypeError('Room unfold function received non-string object.')
    if type(r) != tuple:
        raise TypeError('Room unfold function received non-tuple-like string.')

    rname, rid, mplayer, addr, currplayer, playing = r
    return Room(rname, rid, mplayer, addr, currplayer, playing)
