"""Host server"""
"""Rewriting ~Cynthia"""
import threading
import socket
import random
from . import web_events
from .room import Room
from . import logger
from .web_events import *
from .global_variable import SERVER_HOST, SERVER_PORT, ROOM_PORT, FPS
from pygame.time import Clock

HOST = '127.0.0.1'
HOST_LOGGER = logger.get_public_logger()
SYSTEM = ('SYSTEM', (255,0,0))
COLOR = 1  # Syntax sugar
CLOCK = Clock()


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
        except Exception as e:
            self.exption = e
        finally:
            print(f'Stopping thread {self.name}... ({self.exption if self.exption else None})')
            del self._target, self._args, self._kwargs

    def stop(self):
        self.stopped = True


class Thread(threading.Thread):
    """A stoppable thread"""
    def stop(self):
        raise Exception(f'Stopping thread {self.name}...')


class Chat(object):
    def __init__(self):
        self._record = []

    def __get__(self, instance, owner):
        return self._record

    def add_line(self, sender:tuple, message:str):
        self._record.append((sender, message))


def main(room_name, max_players):
    global threads, host_room, chat, status
    HOST_LOGGER.info('Host running!')
    host_room = create_room(room_name, max_players)

    host_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_sock.bind((HOST, ROOM_PORT))
    threads = {'LISTEN': LoopingThread(target=listen, args=(host_sock,), name='LISTEN')}
    threads['LISTEN'].run()
    HOST_LOGGER.debug('Thread "LISTEN" run!')

    chat = Chat()
    HOST_LOGGER.debug('Chat created!')
    status = 'LOBBY'

    while status == 'LOBBY':
        CLOCK.tick(FPS)


def listen(sock: socket.socket):
    HOST_LOGGER.debug('Another loop of listening!')
    sock.listen()  # Parameter backlog is optional
    conn, addr = sock.accept()
    threads[(conn, addr)] = Thread(target=handle, args=(conn, addr))
    threads[(conn, addr)].run()


def handle(conn:socket.socket, addr:tuple):
    HOST_LOGGER.info(f'Handling connection from {addr}')
    player_ip = addr[0]
    if addr not in host_room.current_players.keys():  # When an address connects host server for the first time,
                                                      # It wants to join the room
        if host_room.max_players <= len(host_room.current_players):  # If the room is full
            send_event(conn, FULL_ERROR)  # Then tell them
        else:
            add_player(conn, player_ip)
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.connect((SERVER_HOST, SERVER_PORT))
            send_event(server_sock, UpdateRoomEvent(current_players=host_room.current_players))
            reply = unfold(server_sock.recv(1024))
            if reply != REQUEST_COMPLETE:
                raise WebEventError('Request is not complete.')
    else:
        request = conn.recv(1024)
        event = unfold(request)
        event_type = event.__class__


def create_room(room_name, max_players):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect((SERVER_HOST, SERVER_PORT))
    HOST_LOGGER.debug('Requesting room id.')
    send_event(server_sock, CreateRoomEvent(room_name, max_players))
    reply = unfold(server_sock.recv(1024))
    if reply.__class__ == Error:
        raise OverflowError('Main server overflow.')
    elif reply.__class__ == RoomEvent:
        room_id = int(reply.content)
        HOST_LOGGER.debug(f'ID: {room_id}')
    host_room = Room(room_name, room_id, max_players, address=HOST)
    HOST_LOGGER.info('Room created!')
    return host_room


def get_color():
    existing_colors = [player[COLOR] for player in list(host_room.current_players.values())] \
                      + [SYSTEM[COLOR]]
    new_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    while new_color in existing_colors:
        new_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return new_color


def add_player(conn, player_ip):
    send_event(conn, RoomEvent(str(host_room)))
    # Give client the room instance (Including the host address)
    player_name = unfold(conn.recv(1024)).message  # Receive player name
    player_color = get_color()
    host_room.add_player(player_name, player_ip, player_color)  # Add the player
    HOST_LOGGER.info(f'Player "{player_name}" ({player_ip}) joined the room.')
    chat.add_line(SYSTEM, f'Player "`${"%02x%02x%02x" % player_color}${player_name}`" joined the room.')
    # Add some color to their name
