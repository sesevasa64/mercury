import core
from socket import *
from core import AsyncSocket
from typing import Coroutine

__all__ = (
    'BasicTCPServer',
)

class BasicTCPServer:
    def __init__(self, address, port, queue_size):
        self.socket = AsyncSocket.create(AF_INET, SOCK_STREAM)
        self.socket.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.socket.bind((address, port))
        self.queue_size = queue_size
    async def listener(self, client_handler: Coroutine):
        self.socket.socket.listen(self.queue_size)
        try:
            while True:
                client, address = await self.socket.accept()
                core.add_coroutine(client_handler(client, address))
        except KeyboardInterrupt:
            pass
        self.socket.socket.close()
