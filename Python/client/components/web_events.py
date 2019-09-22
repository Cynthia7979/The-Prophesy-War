class WebEvent(object):
    def __init__(self, head, content):
        self.head = head
        self.content = content

    def __str__(self):
        return f'{self.head}|{self.content}'

    def unfold(content: str):
        return WebEvent('none', content)


class DrawCardEvent(WebEvent):
    def __init__(self, card_type, card_id: int):
        super().__init__('draw', f'{card_type}_{card_id}')
        self.card_type = card_type
        self.card_id = card_id

    def unfold(content: str):
        try:
            content.index('_')
        except ValueError:
            raise ValueError(f'"{content}" is not an available DrawCardEvent content')
        card_type, card_id = content.split('_')
        return DrawCardEvent(card_type, card_id)


class Prophesy(WebEvent):
    def __init__(self, selections: (tuple, list)):
        super().__init__('prop', ' '.join(selections))
        self.selections = selections

    def unfold(content: str):
        return Prophesy(content.split())


head_map = {'draw': DrawCardEvent, 'prop': Prophesy}


def unfold(e: WebEvent):
    s = str(e)
    try:
        s.index('|')
    except ValueError:
        raise ValueError(f'"{s}" is not a valid WebEvent')
    head, content = s.split('|')
    return head_map[head].unfold(content)


if __name__ == '__main__':
    e = Prophesy(('one', 'two', 'three'))
    print(e)
    u = unfold(e)
    print(u)
    print(u.__dict__)
