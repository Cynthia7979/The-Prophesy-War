# -*- coding: gb2312 -*-


class Human:
    """

    """
    def __init__(self, name: str, luck: int):
        self.name = name
        self._luck = luck  # 运气值
        self._spirit = []  # 上身灵体数组 class: Spirit


class NPC(Human):
    def __init__(self, name, luck):
        Human.__init__(self, name, luck)
        self._fate: int    # 运势值
        self.mission = []  # 持有任务 class: Mission


class Player(Human):
    """
    金币
    声望
    分数
    手牌
    持有NPC
    已接任务

    """
    def __init__(self, name, id):
        Human.__init__(self, name, luck=0)
        self.coin: int
        self.prestige: int  # 声望
        self.owned_npc: []  # class: NPC
        self.hand: []       # class: Card
        self.mission: []     # 任务
        self.id = id
