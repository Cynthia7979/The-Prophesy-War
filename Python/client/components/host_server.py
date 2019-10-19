"""Host server"""
"""Too much mistakes, I suggest rewrite ~Cynthia"""
import threading
import socket
import selectors
import random
from . import room, human, board, web_events
from .global_variable import *
from .web_events import unfold

HOST = '127.0.0.1'


class Host:
    def __init__(self, room_name, max_players, server):
        if max_players <= 1:
            raise ValueError(f'Max player of a room cannot be under or equal to 1 ({max_players})')
        self.server = server
        self.lobby = self.server.create_room(room_name, max_players) #room.Room(room_name, SERVER.get_id(), max_player)
        self.players = {}  # {(conn, addr): playerid}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.board = board.Board()
        self.unused_id = {x:1 for x in range(max_players)}  # Pseudo bitmap
        threads['listening'] = threading.Thread(target=self.listen)

    def start(self):
        self.lobby.set_state(playing=True)

    def set_max_player(self, max_players):
        if max_players > self.lobby.max_players:
            self.unused_id.update({x:1 for x in range(self.lobby.max_players+1, max_players+1)})
        elif max_players < self.lobby.max_players:
            if len(self.players) > max_players:
                raise ValueError(f'Current player # {len(self.players)} is larger than specified max player #, please'
                                 f'verify before changing it.')
            else:
                self.unused_id = dict(tuple(self.lobby.max_players.items())[:max_players])
        else:
            return
        self.lobby.set_state(max_players=max_players)

    def listen(self):
        while True:
            self.socket.listen(8)
            conn, addr = self.socket.accept()
            if (conn, addr) in self.players:
                #                         playerid
                threads[f'handle_{self.players[(conn,addr)]}'] = threading.Thread(target=self.handle, args=(conn, addr))
            else:
                if len(self.players) >= self.lobby.max_players:
                    conn.sendall(web_events.FULL_ERROR)
                    continue
                else:
                    conn.sendall(web_events.JOIN_ACCEPTED)
                name = unfold(conn.recv(1024)).content()
                new_player = human.Player(name, self.get_unused_id())
                self.board.add_player(new_player)
                self.lobby.add_player(new_player.name)
                self.players[(conn, addr)] = new_player.id
                print(new_player.name)

    def get_unused_id(self):
        values = list(self.unused_id.values())
        keys = list(self.unused_id.keys())
        for i, state in enumerate(values):
            if state == 1:
                found = keys[i]
                self.unused_id[found] = 0
                return found
            elif state == 0:
                pass
            else:
                raise ValueError(f'Unexpected value {state} found in unused_id')
        raise ValueError('unused_id ended unexpectedly')

    def handle(self, conn, addr):
        conn.sendall(web_events.CONN_ACCEPTED)
        data = web_events.unfold(conn.recv(1024))
        #TODO


class Server:
    def __init__(self, sock: socket.socket):
        self.sock = sock

    def create_room(self, room_name, max_players):
        self.sock.sendall(bytes(str(web_events.CreateRoomEvent(room_name, max_players))))
        receive = unfold(self.sock.recv(1024))
        if type(receive) == web_events.Error:
            raise web_events.WebEventError(receive.content)


def main(max_players, room_name):
    global threads, SERVER
    threads = {}
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.connect((SERVER, PORT))
    SERVER = Server(sock)
    host = Host(max_players, room_name, SERVER)

