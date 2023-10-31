import os
import typing as t
from typing import Optional

from flask import Flask

from Flask_FrameMVC.AppFactory import factories
from Flask_FrameMVC.Scanner.scan import scan_config, scan_servlet, scan_servlet_out_context, scan_router
from Flask_FrameMVC.Scanner.load import load_config, load_servlet, load_router
from Flask_FrameMVC.core.Exception.Exceptions import BootException
from Flask_FrameMVC.core.Exception.handler import handle_exception
from Flask_FrameMVC.default.config.ServletConfig import ServletConfig
from Flask_FrameMVC.default.config.SwaggerConfig import SwaggerConfig
from Flask_FrameMVC.default.router.PluginHttpRouter import PluginHttpRouter
from Flask_FrameMVC.default.router.TestHttpRouter import TestHttpRouter
from Flask_FrameMVC.ConfigContainer import configs, routers

configs.append(ServletConfig)
configs.append(SwaggerConfig)
routers.append(PluginHttpRouter)
routers.append(TestHttpRouter)


class AppConfig:

    def __init__(self):
        self.app: Optional[Flask] = None

        self.path_dir_code = None

    def init_flask_bootframe(self):
        self._load_config()     # 这顺序有讲究的，不能乱改，尤其config和servlet之间的顺序，跟wsgi_app有关
        self._load_servlet_out_context()
        self._load_servlet()
        self._load_router_http()
        self.app.errorhandler(BootException)(handle_exception)

        return self

    def _load_config(self):
        scan_config(self.path_dir_code)  # 配置初始化
        load_config(self.app)

    def _load_servlet_out_context(self):
        scan_servlet_out_context(self.path_dir_code)

    def _load_servlet(self):
        scan_servlet(self.path_dir_code)
        load_servlet(self.app)

    def _load_router_http(self):
        scan_router(self.path_dir_code)
        load_router(self.app)

    def run(
            self,
            host: t.Optional[str] = None,
            port: t.Optional[int] = None,
            debug: t.Optional[bool] = None,
            load_dotenv: bool = True,
            **options: t.Any,
    ) -> None:
        self.app.run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

    def __call__(self, name, path, model='http'):
        self.app = factories[model](name)
        self.path_dir_code = os.path.abspath(path).replace('main.py', '')
        self.app.path_project = self.path_dir_code

        return self


AppContainer = AppConfig()


__all__ = [
    'AppContainer'
]
