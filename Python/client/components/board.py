import pygame


class Board(object):
    """
    The gameboard.
    """

    def __init__(self, board_id: int, players: list):
        self.board_id = board_id
        self.players = players
        self.shop = []


