from enum import Enum
from .base_scheduler import BaseScheduler

__all__ = ('StopObject', 'BaseHandler')

class StopObject(Enum):
    socket = 0
    future = 1
    sleep  = 2
    winput = 3

# Interface for all handlelrs
class BaseHandler:
    def __init__(self, scheduler: BaseScheduler):
        self.scheduler = scheduler
    def add_object(self, object, task):
        raise NotImplementedError()
    def proceed(self):
        raise NotImplementedError()
    def __bool__(self):
        raise NotImplementedError()
    def acceptable(self):
        raise NotImplementedError()
