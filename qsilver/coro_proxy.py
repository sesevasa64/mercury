from .base_scheduler import CancelCoroutine
from typing import Coroutine

__all__ = ('CoroProxy', 'SendProxy', 'CancelProxy')

class CoroProxy:
    def __init__(self, coro: Coroutine):
        self.coro = coro
    def __eq__(self, other: 'CoroProxy'):
        return self.coro == other.coro
    def getfullname(self):
        return self.coro.__qualname__
    def resume():
        return NotImplementedError()
    def __hash__(self) -> int:
        return hash(self.coro)

class SendProxy(CoroProxy):
    def __init__(self, coro: Coroutine):
        super().__init__(coro)
    def resume(self):
        return self.coro.send(None)

class CancelProxy(CoroProxy):
    def __init__(self, coro: Coroutine):
        super().__init__(coro)
    def resume(self):
        return self.coro.throw(CancelCoroutine)
