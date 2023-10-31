import os

from abc import ABCMeta, abstractmethod

from flask import Blueprint
from flask_restful import Resource, Api
from flask_socketio import Namespace
from typing import Optional, Dict, Type, TypeVar

from Flask_FrameMVC.default.controller.PluginHttpController import PluginHttpController


T = TypeVar('T', bound=Resource)
T_websocket = TypeVar('T_websocket', bound=Namespace)


class BasicInteraction(metaclass=ABCMeta):
    """
    交互层基类
    """

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    @abstractmethod
    def init_app(self, app):
        ...


class BasicWebsocketRouter(BasicInteraction):

    def __init__(self, app=None):
        self.url: Optional[str] = None
        self.resource: Optional[T_websocket] = None
        super().__init__(app)

    def init_app(self, app):
        if getattr(self.app, 'socketio', None):
            self.register()
            self.bind()

    def bind(self):
        self.app.socketio.on_namespace(self.resource(self.url))

    @abstractmethod
    def register(self):
        ...


class BasicHttpRouter(BasicInteraction):
    """
    交互层下的http路由交互基类
    """

    def __init__(self, app=None):
        self.dict_resource: Optional[Dict[str, Type[T]]] = None
        self.name_bp: Optional[str] = None
        self.url_prefix: Optional[str] = None
        super().__init__(app)

    def init_app(self, app):
        self.register()
        self.bind()

    def bind(self):
        if not self.dict_resource or not self.name_bp or not self.url_prefix:
            raise ValueError('name_bp、url_prefix、dict_resource cannot be None')

        if '/' not in self.url_prefix:
            raise ValueError('url_prefix must contain \'/\'')

        blueprint = Blueprint(self.name_bp.replace('.py', ''), __name__, url_prefix=self.url_prefix)
        api = Api(blueprint)

        for url, resource_cls in self.dict_resource.items():
            # 为resource加入get、post、put、patch、delete请求的swagger
            # 排除内置controller，因为它们是为开发者提供开发服务的，不是让开发者去和别方交流对接的，所以应当隐藏
            self._start_swagger(resource_cls)
            api.add_resource(resource_cls, url)

        self.app.register_blueprint(blueprint, url_prefix=self.url_prefix)

    def _start_swagger(self, resource_cls):
        # TODO: 后续需要根据项目的运行模式决定是否开启
        """

        :param resource_cls:
        :return:
        """
        def update_swagger_doc(path_folder, f):
            """

            :param path_folder: path_folder_swagger
            :param f: func
            :return:
            """
            if f and os.path.exists(path_folder + f.__name__ + '.yml'):
                if f.__doc__ is not None:
                    if ':return:' not in f.__doc__:
                        f.__doc__ += '\nfile:' + path_folder + f.__name__ + '.yml'
                    else:
                        f.__doc__ = f.__doc__.replace(
                            ':return:', '\nfile:' + path_folder + f.__name__ + '.yml\n:return:')
                else:
                    f.__doc__ = 'file:' + path_folder + f.__name__ + '.yml'
        if resource_cls in [PluginHttpController]:
            return 0

        path_folder_swagger = self.app.path_project + 'resources/swagger/' + resource_cls.__name__ + '/'
        methods = ['post', 'get', 'put', 'patch', 'delete']

        for method in methods:
            func = resource_cls.__dict__.get(method, None)
            update_swagger_doc(path_folder_swagger, func)

    @abstractmethod
    def register(self):
        ...
