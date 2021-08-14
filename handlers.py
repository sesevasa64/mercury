from enum import Enum
from select import select
from socket import socket
from concurrent.futures import Future
from .base_handler import BaseHandler, StopObject
from .base_scheduler import BaseScheduler
from .yield_proxy import YieldProxy

__all__ = (
    'SocketEvent', 'SocketProxy', 'SocketHandler',
    'FutureHandler', 'SleepHandler', 'AsyncSocket',
    'WindowsInputHandler'
)

BUFFER_SIZE = 256

class SocketEvent(Enum):
    recv = 0
    send = 1

class SocketProxy:
    def __init__(self, socket, event):
        self.socket = socket
        self.event = event

class SocketHandler(BaseHandler):
    def __init__(self, sched: BaseScheduler):
        super().__init__(sched)
        self._select_timeout = 0.01
        self.recv_wait = {}
        self.send_wait = {}
        self.route = {
            SocketEvent.recv: self.recv_wait,
            SocketEvent.send: self.send_wait,
        }
    def add_object(self, socket: SocketProxy, task):
        self.waiting_dict = self.route[socket.event]
        self.waiting_dict[socket.socket] = task
    def proceed(self):
        can_recv, can_send, _ = select(self.recv_wait, self.send_wait, [], self._select_timeout)
        for r in can_recv:
            self.scheduler.add_proxy(self.recv_wait.pop(r))
        for s in can_send:
            self.scheduler.add_proxy(self.send_wait.pop(s))
    def __bool__(self):
        return any((self.recv_wait, self.send_wait))
    def acceptable(self):
        return StopObject.socket

class FutureHandler(BaseHandler):
    def __init__(self, sched: BaseScheduler):
        super().__init__(sched)
        self.future_wait = {}
    def add_object(self, future: Future, task):
        def future_done(future):
            task = self.future_wait.pop(future)
            self.scheduler.add_proxy(task)
        self.future_wait[future] = task
        future.add_done_callback(future_done)
    def proceed(self):
        pass
    def __bool__(self):
        return bool(self.future_wait)
    def acceptable(self):
        return StopObject.future

class SleepHandler(BaseHandler):
    def __init__(self, sched: BaseScheduler):
        super().__init__(sched)
        self.sleeping = []
    def add_object(self, _, task):
        self.sleeping.append(task)
    def proceed(self):
        for i in range(len(self.sleeping)):
            task = self.sleeping[i]
            self.scheduler.add_proxy(task)
            self.sleeping.remove(task)
    def __bool__(self):
        return False
    def acceptable(self):
        return StopObject.sleep

class WindowsInputHandler(BaseHandler):
    def __init__(self, sched: BaseScheduler):
        super().__init__(sched)
        self.waiting = []
    def add_object(self, handler, task):
        self.waiting.append((handler, task))
    def proceed(self):
        for handle, task in self.waiting:
            res = handle.PeekConsoleInput(15)
            if len(res) == 0:
                break
            entry = res[0]
            # Console is in focus
            if entry.EventType == 16:
                handle.ReadConsoleInput(1)
            # User press/release key
            elif entry.EventType == 1:
                # Skip pressing key
                if entry.KeyDown != True or ord(entry.Char) == 0:
                    handle.ReadConsoleInput(1)
                    continue
                self.scheduler.add_proxy(task)
                self.waiting.remove((handle, task))
    def __bool__(self):
        return bool(self.waiting)
    def acceptable(self):
        return StopObject.winput

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
