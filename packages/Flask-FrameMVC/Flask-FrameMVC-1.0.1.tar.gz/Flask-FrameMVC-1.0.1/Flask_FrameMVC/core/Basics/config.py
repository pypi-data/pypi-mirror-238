from typing import Optional

from abc import ABCMeta, abstractmethod


class BasicConfig(metaclass=ABCMeta):
    """
    基础设施层基类
    """

    sort: Optional[int] = None

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    @abstractmethod
    def init_app(self, app):
        # 实际上就是达到了配置类对应的配置内容加载效果
        ...
