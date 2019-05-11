
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
    _name: str #卡名
    _type: str
    _rarity: int
    _tag: [str]
    _description: str #背景描述
    _effect_description: str #效果描述
    #_bg_image: #背景图片
    #_effect_ID: int #效果ID


class ItemCard(Card):
    """
    道具卡
    """


class RitualCard(Card):
    """
    仪式卡
    """

