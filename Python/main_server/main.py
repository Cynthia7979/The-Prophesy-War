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
import logger

HOST = '127.0.0.1'
PORT = 50000


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
    rooms = {}  # {(host, port): Room instance}
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    threads = {'LISTEN': LoopingThread(target=listen, args=(sock,), name='LISTEN')}
    threads['LISTEN'].run()


def listen(sock: socket.socket):
    print('Another loop of listening!')
    sock.listen()  # Parameter backlog is optional
    conn, addr = sock.accept()
    threads[(conn, addr)] = Thread(target=handle, args=(conn, addr))
    threads[(conn, addr)].run()


def handle(conn:socket.socket, addr:tuple):
    print('Handling connection from ', addr)
    request = conn.recv(1024)
    event = unfold(request)
    print(event.__class__)


if __name__ == '__main__':
    main()
