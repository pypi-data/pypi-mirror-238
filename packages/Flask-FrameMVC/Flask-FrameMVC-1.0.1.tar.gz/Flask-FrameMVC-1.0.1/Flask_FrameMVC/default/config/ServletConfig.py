from flask import Flask

from Flask_FrameMVC.core.Basics import BasicConfig
from Flask_FrameMVC.core.servlet.BootMiddleWare import BootMiddleware


class ServletConfig(BasicConfig):

    def init_app(self, app: Flask):
        app.wsgi_app = BootMiddleware(app.wsgi_app)
