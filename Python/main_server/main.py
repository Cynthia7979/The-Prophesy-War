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
    dummy_room = room.Room("r", 2, 8)  # name=r, id=2, maxPlayer=8,
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
    PUBLIC_LOGGER.debug(str(type(addr)))
    threads[(conn, addr)] = Thread(target=handle, args=(conn, addr))
    threads[(conn, addr)].run()


def handle(conn:socket.socket, addr:tuple):
    PUBLIC_LOGGER.info(f'Handling connection from {addr}')
    request = conn.recv(1024)
    event = unfold(request)

    # dummy room testing related START
    rooms[2].set_address((HOST, PORT))
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
    elif event.__class__ == web_events.Prophesy():
        try:
            web_events.send_event(conn, web_events.Prophesy(f'{(0,0),[1,2,3]}'))   # placeholder
        except KeyError:
            web_events.send_event(conn, web_events.Error(f'keyerror for Prophesy'))
            return


if __name__ == '__main__':
    main()
