from typing import Optional
from abc import ABCMeta, abstractmethod

from flask import Flask


class BasicFactory(metaclass=ABCMeta):

    def __init__(self):
        self.app: Optional[Flask] = None

    @abstractmethod
    def __call__(self, name) -> Flask:
        ...

    @abstractmethod
    def run(self, *args):
        ...
