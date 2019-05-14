import pygame
import logger
import socket
import sys, os

PORT = 50000
SERVER = '127.0.0.1'  # In this case, localhost
public_logger = logger.get_public_logger()


def main():
    while True:
        action = menu()
        if action == 'create':
            pass
        elif action == 'join':
            pass
        elif action == 'setting':
            setting()
        elif action == 'exit':
            break
    logger.exit()
    sys.exit()


def menu():
    """
    Pseudo code:

    while True:
        display.display(background, createRoomButton, joinRoomButton, settingButton, exitButton)
        if clicked(createRoomButton):
            return 'create'
        elif clicked(joinRoomButton):
            return 'join'
        elif clicked(settingButton):
            return 'setting'
        elif clicked(exitButton):
            return 'exit'
        update(display)
    """
    return ""


def setting():
    pass


def game(sock):
    pass


def connect():
    sock = socket.socket()
    sock.connect(SERVER)


def receive_game_data(sock):
    pass

