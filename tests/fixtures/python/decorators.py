@property
def value(self):
    return self._value

@staticmethod
def static_method():
    pass

@classmethod
def class_method(cls):
    pass

@decorator_with_args(x=1, y=2)
def decorated():
    pass

@functools.lru_cache(maxsize=128)
def cached_func():
    pass
