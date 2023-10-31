from typing import Optional

from abc import ABCMeta, abstractmethod


class BasicServlet(metaclass=ABCMeta):
    """
    拦截器层
    """
    sort: Optional[int] = None

    @abstractmethod
    def __call__(self, *args, **kwargs):
        # 用于实现拦截器运行，必须实现
        ...


class OutContextBeforeServlet(BasicServlet):
    """
    拦截器层下的上下文外前置拦截器
    """

    @abstractmethod
    def __call__(self, environ, start_response):
        ...


class OutContextBackServlet(BasicServlet):
    """
    拦截器层的上下文外后置拦截器
    """

    @abstractmethod
    def __call__(self, response):
        ...


class BeforeServlet(BasicServlet):
    """
    拦截器层上下文内前置拦截器
    """

    @abstractmethod
    def __call__(self):
        ...


class BackServlet(BasicServlet):
    """
    拦截器层上下文内后置拦截器
    """

    @abstractmethod
    def __call__(self, response):
        ...
