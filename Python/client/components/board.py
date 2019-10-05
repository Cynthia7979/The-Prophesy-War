import pygame


class Board(object):
    """
    The gameboard.
    """

    def __init__(self, players=[]):
        self.players = players
        self.shop = []

    def add_player(self, player_object):
        self.players.append(player_object)



