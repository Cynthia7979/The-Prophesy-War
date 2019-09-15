import sys, os


class BoardObject(object):
    def __init__(self, name, img, coord, container=()):
        """
        Anything that can be placed on the gameboard
        :param name: Name of the object
        :param img: Image of the object
        :param coord: Coordinate of the object on gameboard in polar coordinates
        :param container: Default container of the object
        """
        self.name = name
        self.img = img
        self.rho, self.theta = coord
        self.container = container


