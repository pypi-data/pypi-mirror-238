import logging
import traceback

from flask import request

from Flask_FrameMVC.core.Basics.controller import BasicController
from Flask_FrameMVC.core.Exception.Exceptions import BootException
from Flask_FrameMVC.default.service.Impl.PluginServiceImpl import PluginServiceImpl


class PluginHttpController(BasicController):

    def post(self):
        """
        用于注册插件
        :return:
        """

        try:
            id_plugin = PluginServiceImpl().register(
                request.args.get('name'),
                request.args.get('address'),
                request.args.get('router_alive'),
                request.args.get('router_before'),
                request.args.get('router_arbiter_around'),
                request.args.get('router_around'),
                request.args.get('router_after'),
                request.args.get('router_after_throwing'),
                request.args.get('version'),
                request.args.get('time_out')
            )
        except BootException:
            raise
        except Exception:
            logging.error(traceback.format_exc())
            raise BootException('注册插件失败')

        return {
            "code": 200,
            "message": '注册成功',
            "data": {
                "id": id_plugin
            }
        }

    def delete(self):
        """
        用于删除插件
        :return:
        """

        try:
            PluginServiceImpl().logout(
                request.args.get('name'),
                request.args.get('version')
            )
        except BootException:
            raise
        except Exception:
            logging.error(traceback.format_exc())
            raise BootException('注销插件失败')

        return {
            "code": 200,
            "message": '注销成功'
        }
