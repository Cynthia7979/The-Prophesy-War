# -*- coding: gb2312 -*-
from .global_variable import *


class Hand:
    def __init__(self, cards:tuple=()):
        self.cards = list(cards)

    def get_cards(self):
        return self.cards





