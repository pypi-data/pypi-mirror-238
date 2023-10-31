import logging

import typing as t

from flask_socketio import SocketIO
from flask import Flask

from Flask_FrameMVC.AppFactory.basic import BasicFactory


class WebsocketFactory(BasicFactory):

    def __call__(self, name):
        self.app = Flask(name)
        socketio = SocketIO()
        socketio.init_app(self.app)
        self.app.socketio = socketio

        self.app.run = self.run

        return self.app

    def run(
            self,
            host: t.Optional[str] = None,
            port: t.Optional[int] = None,
            debug: t.Optional[bool] = None,
            load_dotenv: bool = True,
            **options: t.Any,
    ):
        logging.info('进入websocket运行状态')
        self.app.socketio.run(self.app, host=host, port=port, debug=debug, **options)
