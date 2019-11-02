# -*- coding: gb2312 -*-
"""
The Cards
"""
from .global_variable import *


foreground = image('./resources/foreground.png', CARD_DIMENSION)


class Card:
    """Base class of gamecards."""
    def __init__(self, name, kind, rarity, countdown, description, effect_description, effect,
                 background_img: pygame.Surface, foreground_img: pygame.Surface, tag=()):
        """
        Returns a `Card` object.
        The Chinese words below refer to the description of this part in SCP-CN-505 doc.
        :param name: 名称. Name of the card.
        :param kind: 类型. Kind of the card.
        :param rarity: 稀有度. Rarity of the card, range: Item 1~5, Ritual 1~3.
        :param countdown: How many times you can use this card.
        :param description: 介绍. The description of this card.
        :param effect_description: 效果. The description of the effect of this card.
        :param effect: The effect of this card.
        :param background_img: The background of this card.
        :param foreground_img: Foreground of this card. Usually client/resources/foreground.png
        :param tag: 标签. Tuple of tags in strings. Default `()`.
        """
        if tag:
            self._tag = tag
        self.name = name
        self.type = kind
        self._rarity = rarity
        self._countdown = countdown
        self._description = description
        self._effect_description = effect_description
        self._effect = effect
        self._bg = background_img
        self._fg = foreground_img
        self.image = self.get_image()

    def __set__(self, instance, value):
        """
        `Card` instances are immutable. Raises `TypeError`.
        """
        raise TypeError(f'Card instance cannot change value: {instance} -> {value}')

    def activate(self, board):
        """
        Uses the card
        Needs the gameboard because a card changes things on the board.
        :param board: The gameboard.
        """
        self._effect.activate(board)
        self._countdown -= 1
        if self._countdown <= 0:
            return False  # Expired

    # Don't know if does anything but chose to keep it in case.
    # def reset_activation(self, func):
    #     """
    #     Sets the self.activate method
    #     :param func: New activate method
    #     """
    #     ItemCard.activate = func

    def get_image(self):
        """
        Gets the "real" image of the card (AKA mixes foreground and background)
        :return: pygame.Surface
        """
        img_surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), flags=pygame.SRCALPHA)
        img_surf.blit(self._bg, (0,0))
        img_surf.blit(self._fg, (0,0))
        return img_surf


class ItemCard(Card):
    """道具卡"""
    def __init__(self, name, rarity, countdown, description, effect_description, effect, img, tag=None):
        if rarity < 1 or rarity > 5:
            raise ValueError(f'Rarity "{rarity}" out of range (1~5)')
        super().__init__(name, 'item', rarity, countdown, description, effect_description, effect, img,
                         foreground, tag)


class RitualCard(Card):
    """仪式卡"""
    def __init__(self, name, rarity, countdown, description, effect_description, effect, img, tag=None):
        if rarity < 1 or rarity > 3:
            raise ValueError(f'Rarity "{rarity}" out of range (1~3)')
        super().__init__(name, 'ritual', rarity, countdown, description, effect_description, effect, img,
                         foreground, tag)
