# -*- coding: gb2312 -*-

from .spirit import Spirit


class Human:
    """

    """
    def __init__(self, name: str, luck: int):
        name = name
        _luck = luck  # ����ֵ
        _spirit = []  # ������������ class: Spirit


class NPC(Human):
    def __init__(self, name, luck):
        Human.__init__(self, name, luck)
        _fate: int   # ����ֵ
        mission = []  # �������� class: Mission


class Player(Human):
    """
    ���
����
����
����
����NPC
�ѽ�����

    """
    def __init__(self, name, luck):
        Human.__init__(self, name, luck)
        _coin: int
        _prestige: int
        _owned_npc: []  # class: NPC
        _hand: []       # class: Card
        _score: int
        mission: []