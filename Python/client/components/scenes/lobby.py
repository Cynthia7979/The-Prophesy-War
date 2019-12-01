"""
Joins and shows the lobby of a room.
"""
import socket
from .. import logger
from .. import web_events
from ..global_variable import *

#SCENE_LOGGER = logger.get_public_logger('lobby')


def main(room_id):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket instance
    server_sock.connect((SERVER, PORT))  # Connect to main server (blocks the program)
    print('Connected to server!')
    server_sock.sendall(bytes(str(web_events.JoinRoomEvent(room_id)), encoding='utf-8'))  # Ask to join a room.
    print('Join room event sent!')
    r = server_sock.recv(1024)
    r = web_events.unfold(r)

    if r.__class__ == web_events.RoomEvent:
        host_ip = r.message
    elif r.__class__ == web_events.Error:
        return  # TODO Display some error message
    else:
        raise ValueError(f'Received non-Error and non-RoomEvent object from main server: {r.__class__}')

    host_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Use another sock to connect to room
    host_sock.connect((host_ip, PORT))
    reply = host_sock.recv(1024)  # See if we succeed.
    if reply == web_events.FULL_ERROR:
        raise web_events.WebEventError('Room to join is full. This is due to the upper level function which called '
                                       'lobby.main() not verifying the number of players.')
        #                              The scenes/select_room.py should check if the room is already full.
