"""
Main server acts as a transit when:
  * A room is being created
  * A player joins a room
  * A client requests for current list of rooms, and
  * A room updating its status
"""
import threading
import socket
import web_events
from web_events import unfold
from components import logger, room

HOST = 'localhost'
PORT = 50000

PUBLIC_LOGGER = logger.get_public_logger()  # name='server'


class LoopingThread(threading.Thread):
    """A stoppable looping thread"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stopped = False

    def run(self):
        # Copied from the original run method
        try:
            while not self.stopped:  # This line is added
                if self._target:
                    self._target(*self._args, **self._kwargs)
        finally:
            print(f'Stopping thread {self.name}...')
            del self._target, self._args, self._kwargs

    def stop(self):
        self.stopped = True


class Thread(threading.Thread):
    """A stoppable thread"""
    def stop(self):
        raise Exception(f'Stopping thread {self.name}...')


def main():
    global threads, rooms

    PUBLIC_LOGGER.info('Launching server...')


    # dummy room testing related START
    # rooms = {}
    dummy_room = room.Room("r", 2, 8, HOST)  # name=r, id=2, maxPlayer=8, address=HOST
    rooms = {2: dummy_room, 16: dummy_room}  # {id: Room instance}; the dummy room is "Room 3"

    # dummy room testing related FINISH

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))

    threads = {'LISTEN': LoopingThread(target=listen, args=(sock,), name='LISTEN')}
    threads['LISTEN'].run()


def listen(sock: socket.socket):
    PUBLIC_LOGGER.debug('Another loop of listening!')
    sock.listen()  # Parameter backlog is optional
    conn, addr = sock.accept()
    threads[(conn, addr)] = Thread(target=handle, args=(conn, addr))
    threads[(conn, addr)].run()


def handle(conn:socket.socket, addr:tuple):
    PUBLIC_LOGGER.info(f'Handling connection from {addr}')
    try:
        request = conn.recv(1024)
    except ConnectionResetError:
        return
    event = unfold(request)
    ip, port = addr

    # dummy room testing related START
    #rooms[2].address = HOST
    #rooms[2].set_address(addr)

    # dummy room testing related FINISH

    if event.__class__ == web_events.JoinRoomEvent:
        try:
            room = rooms[int(event.room_id)]
            web_events.send_event(conn, web_events.RoomEvent(f'{room.address}'))
        except KeyError:
            web_events.send_event(conn, web_events.Error(f'Cannot find room #{event.room_id}'))
            PUBLIC_LOGGER.info(f'SERVER Cannot find room #{event.room_id}')
            return
    elif event.__class__ == web_events.Prophesy:
        try:
            web_events.send_event(conn, web_events.Prophesy(f'{(0,0),[1,2,3]}'))   # placeholder
        except KeyError:
            web_events.send_event(conn, web_events.Error(f'keyerror for Prophesy'))
            return
    elif event.__class__ == web_events.CreateRoomEvent:
        add_room(event.room_name, event.max_players, ip, conn)


def add_room(room_name, max_players, addr, conn):
    # I will try to switch to bitmap later, if necessary
    all_ids = list(rooms.keys())
    found_id = None
    for i in range(100):
        if i not in all_ids:
            found_id = i
            break
        if i == 100:
            PUBLIC_LOGGER.warning('Too many rooms! New room will not get a new id.')
            web_events.send_event(conn, web_events.Error('Rooms present achieve maximum number (100).'))
    rooms[found_id] = room.Room(room_name, found_id, max_players, addr)
    web_events.send_event(conn, web_events.WebEvent('',found_id))
    PUBLIC_LOGGER.info(f'Room created: "{room_name}" (#{found_id}) with a max player of {max_players}.')


if __name__ == '__main__':
    main()
