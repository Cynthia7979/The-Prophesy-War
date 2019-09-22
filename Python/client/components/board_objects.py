import sys, os


class Container(object):
    def __init__(self, container=()):
        """
        Things in game that has a container
        :param name: Name of the object
        :param container: Default container of the object
        """
        self.container = container


class BoardPlacement(Container):
    def __init__(self, name, img, coord, container=()):
        """
        Anything that can be placed on the gameboard
        :param img: Image of the object
        :param coord: Coordinate of the object on gameboard in polar coordinates
        """
        super().__init__(container)
        self.name = name
        self.img = img
        self.rho, self.theta = coord


class PlayerTerritory(Container):
    def __init__(self, id, theta1, theta2, container=()):
        """
        The "kingdom" of a player where they have citizens and can place things
        :param id: Player ID
        :param theta1:, :param theta2: range of the territory
        :param container: Things in the territory
        """
        super().__init__(container)
        self.id = id
        self.range = (theta1, theta2)
