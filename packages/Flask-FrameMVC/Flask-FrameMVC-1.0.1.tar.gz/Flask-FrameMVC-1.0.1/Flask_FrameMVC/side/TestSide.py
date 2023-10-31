from functools import partial, wraps

from Flask_FrameMVC.side.BasicSide import BasicSide


class MethodTestSide(BasicSide):
    funcs = {}

    @staticmethod
    def before(instance, *args, **kwargs):
        pass

    @staticmethod
    def arbiter_around(instance, *args, **kwargs) -> bool:
        pass

    @staticmethod
    def around(instance, *args, **kwargs) -> dict:
        pass

    @staticmethod
    def after(instance, *args, **kwargs):
        pass

    @staticmethod
    def after_throwing(e, instance, *args, **kwargs) -> dict:
        pass

    def __init__(self, func):
        super().__init__(func)

    def __get__(self, instance, owner):
        self.funcs[self.func.__qualname__.replace('.', '/')] = partial(self.func, instance)

        if instance is None:
            return self
        return partial(self, instance)

    def __call__(self, *args, **kwargs):

        return self.func(*args, **kwargs)


def FunctionTestSide(func):
    MethodTestSide.funcs[func.__name__] = func

    @wraps(func)
    def wrapper(*args, **kwargs):

        return func(*args, **kwargs)

    return wrapper
