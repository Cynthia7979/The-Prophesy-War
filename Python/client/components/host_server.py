"""Host server"""
"""Rewriting ~Cynthia"""
import threading
import socket
from . import web_events
from .room import Room
from . import logger
from .web_events import unfold
from .global_variable import SERVER_HOST, SERVER_PORT, ROOM_PORT

HOST = '127.0.0.1'
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


def main(room_name, max_players):
    global threads, host_room
    HOST_LOGGER.info('Host running!')
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect((SERVER_HOST, SERVER_PORT))
    HOST_LOGGER.debug('Requesting room id.')
    web_events.send_event(server_sock, web_events.CreateRoomEvent(room_name, max_players))
    reply = web_events.unfold(server_sock.recv(1024))
    if reply.__class__ == web_events.Error:
        raise OverflowError('Main server overflow.')
    elif reply.__class__ == web_events.WebEvent:
        room_id = int(reply.content)
    host_room = Room(room_name, room_id, max_players, address=HOST)
    HOST_LOGGER.info('Room created!')

    host_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_sock.bind((HOST, ROOM_PORT))
    threads = {'LISTEN': LoopingThread(target=listen, args=(host_sock,), name='LISTEN')}
    threads['LISTEN'].run()


def listen(sock: socket.socket):
    HOST_LOGGER.debug('Another loop of listening!')
    sock.listen()  # Parameter backlog is optional
    conn, addr = sock.accept()
    threads[(conn, addr)] = Thread(target=handle, args=(conn, addr))
    threads[(conn, addr)].run()


def handle(conn:socket.socket, addr:tuple):
    HOST_LOGGER.info(f'Handling connection from {addr}')
    if addr not in host_room.current_players.keys():  # When an address connects host server for the first time,
                                                      # It wants to join the room
        if host_room.max_players >= len(host_room.current_players):  # If the room is full
            web_events.send_event(conn, web_events.FULL_ERROR)  # Then tell them
            player_name = conn.recv(1024)
            host_room.add_player(player_name, )
        else:
            web_events.send_event(conn, web_events.RoomEvent(str(host_room)))  # Give client the room instance
                                                                               # (Including the host address)
    request = conn.recv(1024)
    event = unfold(request)
    event_type = event.__class__
    # if event_type == web_events.JoinRoomEvent:
    #     if self.
