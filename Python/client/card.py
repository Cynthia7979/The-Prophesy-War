# -*- coding: gb2312 -*-


class Card:
    """
类型
稀有度
标签
名称
介绍
效果
正面？/负面？

    """
    _name: str  # 卡名
    _type: str
    _rarity: int
    _tag: [str]
    _description: str  # 背景描述
    _effect_description: str  # 效果描述
    # _fg_image: #前景图片
    # _bg_image: #背景图片
    _effect_ID: str  # 效果ID

    def __init__(self, name: str, type: str, rarity: int, tag: [str], description: str,
                 effect_description: str, effect_id: str):
        self._name = name
        self._type = type
        self._rarity = rarity
        self._tag = tag
        self._description = description
        self._effect_description = effect_description
        self._effect_ID = effect_id


class ItemCard(Card):
    """
    道具卡
    """

    def __init__(self, name: str, type: str, rarity: int, tag: [str], description: str,
                 effect_description: str, effect_id: str):
        Card.__init__(self, name, type, rarity, tag, description, effect_description, effect_id)


class RitualCard(Card):
    """
    仪式卡
    """

    def __init__(self, name: str, type: str, rarity: int, tag: [str], description: str,
                 effect_description: str, effect_id: str):
        Card.__init__(self, name, type, rarity, tag, description, effect_description, effect_id)

    def get_effect_id(self):
        return self._effect_ID
