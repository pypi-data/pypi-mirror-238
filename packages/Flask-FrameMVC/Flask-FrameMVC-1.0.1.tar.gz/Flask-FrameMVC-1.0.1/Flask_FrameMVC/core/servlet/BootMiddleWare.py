import json

from Flask_FrameMVC.ConfigContainer import servlets_before_out_context, servlets_back_out_context
from Flask_FrameMVC.core.Exception.Exceptions import BootException


class BootMiddleware:

    def __init__(self, old_wsgi_app):
        self.old_wsgi_app = old_wsgi_app

    def __call__(self, environ, start_response):
        # 请求前拦截器
        try:
            for servlet_bf in servlets_before_out_context:
                servlet_bf(environ, start_response)
        except BootException as e:
            response = {
                "code": e.code,
                "message": e.description
            }
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [json.dumps(response).encode('utf-8')]
        except Exception:
            response = {
                "code": 500,
                "message": "前置拦截器处发生未知错误"
            }
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [json.dumps(response).encode('utf-8')]

        # 请求处理
        response = self.old_wsgi_app(environ, start_response)

        # 请求后拦截器
        try:
            for servlet_bk in servlets_back_out_context:
                response = servlet_bk(response)
        except BootException as e:
            response = {
                "code": e.code,
                "message": e.description
            }
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [json.dumps(response).encode('utf-8')]
        except Exception:
            response = {
                "code": 500,
                "message": "后置拦截器处发生未知错误"
            }
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [json.dumps(response).encode('utf-8')]

        return response
