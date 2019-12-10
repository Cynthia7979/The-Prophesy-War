"""Host server"""
"""Too much problems, I suggest rewrite ~Cynthia"""
import threading
import socket
import selectors
import random
from . import room, human, board, web_events
from . import logger
from .web_events import unfold

HOST = '127.0.0.1'
PORT = 50000
HOST_LOGGER = logger.get_public_logger()


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


def main(room_name, room_id, max_players):
    global threads, host_room
    threads = {}
    host_room = room.Room(room_name, room_id, max_players, address=(HOST, PORT))


def listen(sock: socket.socket):
    HOST_LOGGER.debug('Another loop of listening!')
    sock.listen()  # Parameter backlog is optional
    conn, addr = sock.accept()
    conn.send(bytes("WELCOME TO THE HOST SERVER", "utf-8"))
    threads[(conn, addr)] = Thread(target=handle, args=(conn, addr))
    threads[(conn, addr)].run()


def handle(conn:socket.socket, addr:tuple):
    HOST_LOGGER.info(f'Handling connection from {addr}')
    if addr not in host_room.current_players.keys():
        if host_room.max_players >= len(host_room.current_players):
            web_events.send_event(conn, web_events.FULL_ERROR)
        else:
            web_events.send_event(conn, web_events.RoomEvent(str(host_room)))
    request = conn.recv(1024)
    event = unfold(request)
    #if event.__class__ == web_events.JoinRoomEvent: