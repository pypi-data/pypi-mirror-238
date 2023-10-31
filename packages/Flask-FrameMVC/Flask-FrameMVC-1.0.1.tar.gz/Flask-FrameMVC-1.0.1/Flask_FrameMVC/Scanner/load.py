from flask import Flask

from Flask_FrameMVC.ConfigContainer import configs, routers, servlets_before, servlets_back


def load_config(app: Flask):
    for config in configs:
        config(app)


def load_router(app: Flask):
    for router in routers:
        router(app)


def before_request_func():
    for servlet in servlets_before:
        servlet()


def back_request_func(response):
    for servlet in servlets_back:
        response = servlet(response)

    return response


def load_servlet(app):
    app.before_request(before_request_func)
    app.after_request(back_request_func)
