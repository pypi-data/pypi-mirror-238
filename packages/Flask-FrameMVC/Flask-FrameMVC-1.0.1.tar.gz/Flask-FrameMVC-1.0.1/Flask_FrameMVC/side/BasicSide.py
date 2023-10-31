import traceback
import functools
from abc import ABCMeta, abstractmethod

from Flask_FrameMVC.core.Exception.Exceptions import BootException


class BasicSide(metaclass=ABCMeta):

    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return functools.partial(self, instance)

    @staticmethod
    @abstractmethod
    def before(instance, *args, **kwargs):
        ...

    @staticmethod
    @abstractmethod
    def arbiter_around(instance, *args, **kwargs) -> bool:
        ...

        return False

    @staticmethod
    @abstractmethod
    def around(instance, *args, **kwargs) -> dict:
        ...

    @staticmethod
    @abstractmethod
    def after(instance, *args, **kwargs):
        ...

    @staticmethod
    @abstractmethod
    def after_throwing(e, instance, *args, **kwargs) -> dict:
        ...

    def __call__(self, *args, **kwargs) -> dict:
        args_original = args
        args += (args[0].__class__.__name__+'.'+self.func.__name__,)

        try:
            self.before(*args, **kwargs)
            if self.arbiter_around(*args, **kwargs):
                ret = self.around(*args, **kwargs)
            else:
                ret = self.func(*args_original, **kwargs)
            self.after(*args, **kwargs)
        except BootException:
            raise
        except Exception:
            ret = self.after_throwing(traceback.format_exc(), *args, **kwargs)

        return ret
