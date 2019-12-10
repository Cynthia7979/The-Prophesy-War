"""
Stylized classes to send in socket connections.

**Usage:**
Each class's `head` is used to specify which kind of WebEvent it is. Content is the data you want to transfer.
Also, each class include a different way to unfold (aka. unpack) the string received from socket connections.
If the string style doesn't meet with its head, a `ValueError` will be thrown.

**Note:** Currently, this file should be identical to main_server/web_events.py
"""


class WebEvent(object):
    def __init__(self, head, content):
        self.head = head
        self.content = content

    def __repr__(self):
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


class RoomEvent(WebEvent):

    def __init__(self, message):
        super().__init__('room', message)
        self.message = message

    def unfold(content):
        return RoomEvent(content)


class CreateRoomEvent(WebEvent):
    def __init__(self, room_name, max_players):
        super().__init__('crte', f'{room_name}/{max_players}')
        self.room_name = room_name
        self.max_players = max_players

    def unfold(content:str):
        try:
            content.index('/')
        except ValueError:
            raise ValueError(f'"{content}" is not an available CreateRoomEvent content')
        room_name, max_players = content.split('/')
        return CreateRoomEvent(room_name, max_players)


class JoinRoomEvent(WebEvent):
    def __init__(self, room_id):
        super().__init__('join', room_id)
        self.room_id = room_id

    def unfold(content:str):
        return JoinRoomEvent(content)


class Error(WebEvent):
    def __init__(self, message):
        super().__init__('eror', message)
        self.message = message

    def unfold(content):
        return Error(content)


class WebEventError(Exception):
    pass


head_map = {'draw': DrawCardEvent, 'prop': Prophesy, 'eror': Error, 'room': RoomEvent, 'crte':CreateRoomEvent,
            'join': JoinRoomEvent}  # Link the head to specific `unfold` method.




def unfold(e):
    s = str(e)
    # s = s[1:]  # theres a 'b' at the start, this removes it
    try:
        s.index('|')
    except ValueError:
        raise ValueError(f'"{s}" is not a valid WebEvent')
    head, content = s.split('|')
    head = head.strip("'b")  # Socket connections use `bytes` type, like this: `b'bytes words'`
    head = head.strip('"')   # and also a " <- this quote sign
    content = content[:-1]   # We need to manually remove `b'` at the beginning and `'` in the end

    # b"room|('xxx.xxx.xxx.x\',xxxxx)"
    if head == 'room':      # haven't progressed until others yet, but 'room' need these
        content = content.strip("(")
        content = content.strip('\'')         # and plenty more format thing to remove
        content = content.strip(')')          # im too lazy to comment them 1 by 1,
        comma_index = content.find(',')       # u can see what happens in debug mode
        content = content[:comma_index-1]
                                              # end result is 'xxx.xxx.xxx.xxx'
                                              # which is 'ip'
    try:
        unfold_class = head_map[head]
    except KeyError:
        unfold_class = WebEvent
    return unfold_class.unfold(content)


def send_event(conn, event):
    return conn.sendall(bytes(str(event), encoding='utf-8'))


# Some pre-defined WebEvents to use
CONN_ACCEPTED = WebEvent('none', 'Connection accepted')

FULL_ERROR = Error('Room is Full')

JOIN_ACCEPTED = RoomEvent('Join room request accepted')

if __name__ == '__main__':
    e = Prophesy(('one', 'two', 'three'))
    print(e)
    u = unfold(e)
    print(u)
    print(u.__dict__)
