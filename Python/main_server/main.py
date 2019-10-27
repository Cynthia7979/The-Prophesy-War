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

HOST = '127.0.0.1'
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
    rooms = {}  # {id: Room instance}
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
    request = conn.recv(1024)
    event = unfold(request)
    if event.__class__ == web_events.JoinRoomEvent:
        try:
            room = rooms[event.room_id]
        except KeyError:
            web_events.send_event(web_events.Error(f'Cannot find room #{event.room_id}'))
            return
        web_events.send_event(web_events.RoomEvent(f'{room.address}'))


if __name__ == '__main__':
    main()
