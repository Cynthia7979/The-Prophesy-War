class WebEvent(object):
    def __init__(self, head, content):
        self.head = head
        self.content = content

    def __str__(self):
        return f'{self.head}|{self.content}'


class DrawCardEvent(WebEvent):
    def __init__(self, card_type, card_id):
        super().__init__('draw', f'{card_type}_{card_id}')


class Prophesy(WebEvent):
    def __init__(self, selections):
        super().__init__('prop', selections)


head_map = {'draw': DrawCardEvent, 'prop': Prophesy}


def unfold(s):
    try:
        head, content = s.split('|')
    except ValueError:
        raise ValueError(f'"{s}" is not a valid WebEvent')



if __name__ == '__main__':
    print(str(DrawCardEvent('cardtype', [123,345,567])))
