import socket
from .. import logger
from .. import web_events
from ..global_variable import *

#SCENE_LOGGER = logger.get_public_logger('lobby')


def main(room_id):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect((SERVER, PORT))
    print('Connected to server!')
    server_sock.sendall(bytes(str(web_events.JoinRoomEvent(room_id)), encoding='utf-8'))
    print('Join room event sent!')
    host_ip = server_sock.recv(1024)
    host_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_sock.connect((host_ip, PORT))
    reply = host_sock.recv(1024)
    if reply == web_events.FULL_ERROR:
        raise web_events.WebEventError('Room to join is full. This is due to the upper level function which called '
                                       'lobby.main() not verifying the number of players.')
