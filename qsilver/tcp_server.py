from socket import *
from typing import Coroutine
from .async_socket import AsyncSocket
from .api import add_coroutine, CancelCoroutine

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
                add_coroutine(client_handler(client, address))
        except (KeyboardInterrupt, CancelCoroutine):
            self.socket.socket.close()
