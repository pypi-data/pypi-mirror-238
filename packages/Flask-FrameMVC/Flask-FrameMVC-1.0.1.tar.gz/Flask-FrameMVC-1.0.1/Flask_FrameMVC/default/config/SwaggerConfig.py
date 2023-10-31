from flask import Flask
from flasgger import Swagger

from Flask_FrameMVC.core.Basics import BasicConfig


class SwaggerConfig(BasicConfig):
    swagger = None

    def init_app(self, app: Flask):
        self.swagger = Swagger()
        self.swagger.init_app(app)
