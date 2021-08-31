from typing import Coroutine, Callable

__all__ = ('CancelCoroutine', 'BaseScheduler')

class CancelCoroutine(BaseException):
    pass

class BaseScheduler:
    def add_task(self, task: Callable, *args, **kwargs):
        raise NotImplementedError()
    def add_coro(self, coro: Coroutine):
        raise NotImplementedError()
    def cancel_coro(self, coro: Coroutine):
        raise NotImplementedError()
    def add_proxy(self, proxy):
        raise NotImplementedError()
    def resume(self, proxy):
        raise NotImplementedError()
    def run_forever(self):
        raise NotImplementedError()
