import pygame


class Board(object):
    """
    The gameboard.
    """

    def __init__(self, players=()):
        """
        Returns a `Board` object.
        :param players: List of any players that are "on" the board (in the game) now. Must be consisted of
        `Player` instance
        """
        self.players = list(players)
        self.shop = []

    def add_player(self, player_object):
        """
        Add a player.
        Do not directly modify the `players` property.
        :param player_object: A `Player` instance
        :return: None
        """
        self.players.append(player_object)



