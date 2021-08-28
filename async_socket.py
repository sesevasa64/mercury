from socket import socket
from .yield_proxy import YieldProxy
from .base_handler import StopObject
from .handlers import SocketEvent, SocketProxy

__all__ = (
    'AsyncSocket',
)

class AsyncSocket:
    def __init__(self, socket: socket):
        self.socket = socket
    async def send(self, bytes):
        await YieldProxy((SocketProxy(self.socket, SocketEvent.send), StopObject.socket))
        self.socket.send(bytes)
    async def recv(self, buffer_size):
        await YieldProxy((SocketProxy(self.socket, SocketEvent.recv), StopObject.socket))
        return self.socket.recv(buffer_size)
    async def accept(self):
        await YieldProxy((SocketProxy(self.socket, SocketEvent.recv), StopObject.socket))
        client, address = self.socket.accept()
        return AsyncSocket(client), address
    async def connect(self, address, port):
        await YieldProxy((SocketProxy(self.socket, SocketEvent.send), StopObject.socket))
        self.socket.connect((address, port))
    def __getattr__(self, name: str):
        return getattr(self.socket, name)
    @classmethod
    def create(cls, family=-1, type=-1, proto=-1, fileno=None):
        return cls(socket(family, type, proto, fileno))
