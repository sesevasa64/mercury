import sys
import time
import signal
import threading
from typing import Coroutine, Callable, List, Dict
from concurrent.futures import Future, ProcessPoolExecutor

from .yield_proxy import YieldProxy
from .base_scheduler import CancelCoroutine
from .scheduler import Scheduler, StopObject
from .base_handler import BaseHandler
from .handlers import *

__all__ = (
    'create_scheduler',
    'add_coroutine',
    'cancel_coroutine',
    'get_scheduler',
    'run_forever',
    'set_timeout',
    'AsyncFuture',
    'sleep'
)

_schedulers: Dict[int, Scheduler] = {}

def create_scheduler() -> Scheduler:
    id = threading.current_thread().ident
    if id in _schedulers:
        return _schedulers[id]
    sched = Scheduler()
    for handler in _prepare_headers():
        sched.add_handler(handler)
    _schedulers[id] = sched
    return sched

def add_coroutine(coro: Coroutine):
    sched = get_scheduler()
    sched.add_coro(coro)

def cancel_coroutine(coro: Coroutine):
    sched = get_scheduler()
    sched.cancel_coro(coro)

def get_scheduler() -> Scheduler:
    id = threading.current_thread().ident
    if id not in _schedulers:
        raise ValueError("Scheduler not exist in this thread")
    return _schedulers[id]

def run_forever():
    sched = get_scheduler()
    sched.run_forever()

def keyboard_interrupt(signum, frame):
    sys.exit(0)

def exception_interrupt(signum, frame):
    sys.exit(1)

def init():    
    signal.signal(signal.SIGINT, keyboard_interrupt)
    signal.signal(signal.SIGTERM, exception_interrupt)

class AsyncFuture:
    future_pool = ProcessPoolExecutor(initializer=init)
    def __init__(self, future: Future):
        self.future = future
    async def result(self):
        await YieldProxy((self.future, StopObject.future))
        return self.future.result()
    def cancel(self):
        return self.future.cancel()
    @classmethod
    def from_pool(cls, task: Callable, *args, **kwargs):
        future = cls.future_pool.submit(task, *args, **kwargs)
        return AsyncFuture(future)

async def sleep_old(delay):
    try:
        deadline = time.time() + delay
        while time.time() < deadline:
            await YieldProxy((None, StopObject.sleep))
    except CancelCoroutine:
        raise

async def sleep(delay):
    try:
        deadline = time.time() + delay
        await YieldProxy((deadline, StopObject.sleep))
    except CancelCoroutine:
        raise

def set_timeout(timeout):
    sched = get_scheduler()
    sched.set_timeout(timeout)

def _prepare_headers() -> List[BaseHandler]:
    handlers = [
        SocketHandler, 
        FutureHandler,
        SleepHandler,
    ]
    try:
        import win32api
        handlers.append(WindowsInputHandler) 
    except ImportError:
        pass
    return handlers
