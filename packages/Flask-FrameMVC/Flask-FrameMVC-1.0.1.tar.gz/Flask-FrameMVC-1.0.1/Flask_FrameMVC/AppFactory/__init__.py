from Flask_FrameMVC.AppFactory.http import HttpFactory
from Flask_FrameMVC.AppFactory.websocket import WebsocketFactory


factories = {
    'websocket': WebsocketFactory(),
    'http': HttpFactory()
}
