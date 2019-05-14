# -*- coding: gb2312 -*-

from .spirit import Spirit


class Human:
    """

    """
    def __init__(self, name: str, luck: int):
        name = name
        _luck = luck  # 运气值
        _spirit = []  # 上身灵体数组 class: Spirit


class NPC(Human):
    def __init__(self, name, luck):
        Human.__init__(self, name, luck)
        _fate: int    # 运势值
        mission = []  # 持有任务 class: Mission


class Player(Human):
    """
    金币
    声望
    分数
    手牌
    持有NPC
    已接任务

    """
    def __init__(self, name, luck):
        Human.__init__(self, name, luck)
        coin: int
        prestige: int  # 声望
        owned_npc: []  # class: NPC
        hand: []       # class: Card
        mission: []     # 任务
