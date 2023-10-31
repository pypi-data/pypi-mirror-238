from flask_socketio import Namespace
from flask_restful import Resource


class BasicController(Resource):
    decorators_get = []
    decorators_post = []
    decorators_put = []
    decorators_patch = []
    decorators_delete = []

    method_decorators = {
        'get': decorators_get,
        'post': decorators_post,
        'put': decorators_put,
        'patch': decorators_patch,
        'delete': decorators_delete
    }


class BasicWebsocketController(Namespace):
    ...
