
from spirit import Spirit
from card


class Human:
    """

    """
    _name: str
    _luck: int #运气值
    _spirit_on_body: [Spirit] #上身灵体数组


class NPC(Human):

    _fate: int #运势值
   # _mission: Mission #持有任务


class Player(Human):
    """
    金币
声望
分数
手牌
持有NPC
已接任务

    """
    _coin: int
    _prestige: int
    _owned_npc: [NPC]
    _hand: [Card]
    _score: int
    #_misson: []


