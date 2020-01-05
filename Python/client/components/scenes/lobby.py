"""
Joins and displays the lobby of a room.
"""
import socket
from .. import room
from .. import logger
from .. import web_events
from ..global_variable import *

SCENE_LOGGER = logger.get_public_logger('lobby')


def main(room_id, player_name):
    # Connect to main server
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Server socket
    server_sock.connect((SERVER, PORT))  # Connect to main server (blocks the program)
    SCENE_LOGGER.debug('Connected to server!')
    server_sock.sendall(bytes(str(web_events.JoinRoomEvent(room_id)), encoding='utf-8'))  # Ask to join a room.
    SCENE_LOGGER.debug('Join room event sent!')
    r = server_sock.recv(1024)
    r = web_events.unfold(r)
    if r.__class__ == web_events.RoomEvent:
        host_ip = r.message
        SCENE_LOGGER.debug('Host IP: ' + host_ip)
    elif r.__class__ == web_events.Error:
        PUBLIC_LOGGER.info(f'Server sent back some ERROR')
        return  # TODO Display some error message
    else:
        raise ValueError(f'Received non-Error and non-RoomEvent object from main server: {r.__class__}')

    # Connect to host server
    host_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Use another sock to connect to room
    host_sock.connect((host_ip, PORT))  # If the address is new to the host, it will comprehend it as requesting to
    #                                     join.
    SCENE_LOGGER.debug('Connecting to '+host_ip+'...')
    reply = host_sock.recv(1024)  # See if we succeed.
    if reply == web_events.FULL_ERROR:
        raise web_events.WebEventError('Room to join is full. This is due to the upper level function which called '
                                       'lobby.main() not verifying the number of players.')
        #                              The scenes/select_room.py should check if the room is already full.
    else:
        event = web_events.unfold(reply)
        event_type = event.__class__
        if event_type == web_events.RoomEvent:
            host_room = room.unfold(event.message)  # str -> Room
            SCENE_LOGGER.debug('Received room instance.')
            web_events.send_event(host_sock, web_events.RoomEvent(player_name))

