__all__ = ('YieldProxy', )

class YieldProxy:
    def __init__(self, obj):
        self.obj = obj
    def __await__(self):
        yield self.obj
