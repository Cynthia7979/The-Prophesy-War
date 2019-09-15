# -*- coding: gb2312 -*-
from .global_variable import *


foreground = image('./resources/foreground.png', CARD_DIMENSION)


class Card:
    """Base class"""
    def __init__(self, name, kind, usage, rarity, countdown, description, effect_description, effect,
                 background_img: pygame.Surface, foreground_img: pygame.Surface, tag=None):
        if tag:
            self._tag = tag
        self.name = name
        self.type = kind
        self.usage = usage
        self._rarity = rarity
        self._countdown = countdown
        self._description = description
        self._effect_description = effect_description
        self._effect = effect
        self._bg = background_img
        self._fg = foreground_img
        self.image = self.get_image()

    def __set__(self, instance, value):
        raise TypeError(f'Card instance cannot change value: {instance} -> {value}')

    def activate(self, board):
        self._effect.activate(board)
        self._countdown -= 1
        if self._countdown <= 0:
            return False  # Expired

    def reset_activation(self, func):
        """
        Sets the self.activate method
        :param func: New activate method
        :return: None
        """
        ItemCard.activate = func

    def get_image(self):
        img_surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), flags=pygame.SRCALPHA)
        img_surf.blit(self._bg, (0,0))
        img_surf.blit(self._fg, (0,0))
        return img_surf


class ItemCard(Card):
    """道具卡"""
    def __init__(self, name, usage, rarity, countdown, description, effect_description, effect, img, tag=None):
        if rarity < 1 or rarity > 5:
            raise ValueError(f'Rarity "{rarity}" out of range (1~5)')
        super().__init__(name, 'item', usage, rarity, countdown, description, effect_description, effect, img,
                         foreground, tag)


class RitualCard(Card):
    """仪式卡"""
    def __init__(self, name, usage, rarity, countdown, description, effect_description, effect, img, tag=None):
        if rarity < 1 or rarity > 3:
            raise ValueError(f'Rarity "{rarity}" out of range (1~3)')
        super().__init__(name, 'ritual', usage, rarity, countdown, description, effect_description, effect, img,
                         foreground, tag)
