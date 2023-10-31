import traceback
import logging
import json
import requests
from typing import Optional

from Flask_FrameMVC.core.Exception.Exceptions import BootException
from Flask_FrameMVC.side.BasicSide import BasicSide
from Flask_FrameMVC.default.dao.PluginDao import PluginDao


headers = {
            'content-type': 'application/json;charset=utf-8'
        }


class PluginSide(BasicSide):
    """
    该侧面实现，对于系统来说，是侧面机制的具体实现，对插件来说，则是插件管理器的具体实现
    """

    def __init__(self, func):
        self.list_plugins: Optional[list] = None    # 这个容器本质上起到了插件总线的作用，只不过该总线只确保插件与系统之间的通讯/数据交互，不提供插件与插件之间的通讯
        super().__init__(func)

    def before(self, instance, *args, **kwargs):
        point_extension = args[-1]
        with PluginDao() as dao:
            self.list_plugins = [
                {
                    'id': plugin.id,
                    'name': plugin.name,
                    'version': plugin.pluginmeta.version,
                    'point_extension': point_extension,
                    'timeout': plugin.pluginmeta.time_out,
                    'alive': plugin.pluginrouter.alive,
                    'before': plugin.pluginrouter.before,
                    'arbiter_around': plugin.pluginrouter.arbiter_around,
                    'around': plugin.pluginrouter.around,
                    'after': plugin.pluginrouter.after,
                    'after_throwing': plugin.pluginrouter.after_throwing
                } for plugin in dao.select_list_plugins_by_point_extension(point_extension)
            ]

        for info_plugin in self.list_plugins:
            try:
                response = requests.post(
                    url=info_plugin['alive'],
                    headers=headers,
                    data=json.dumps(info_plugin),
                    timeout=info_plugin['timeout']
                )
                if response.status_code == 200:
                    ...
                else:
                    del info_plugin['alive']
            except requests.exceptions.Timeout:
                try:
                    response = requests.post(
                        url=info_plugin['alive'],
                        headers=headers,
                        data=json.dumps(info_plugin),
                        timeout=info_plugin['timeout']
                    )
                    if response.status_code == 200:
                        ...
                    else:
                        del info_plugin['alive']
                except requests.exceptions.Timeout:
                    logging.info(f'插件{info_plugin["name"]}:{info_plugin["version"]}通讯超时')
                    del info_plugin['alive']
                except Exception:
                    logging.error(f'插件{info_plugin["name"]}:{info_plugin["version"]}执行before步骤时失败')
                    logging.error(traceback.format_exc())
                    del info_plugin['alive']
            except BootException:
                raise
            except Exception:
                logging.error(f'插件{info_plugin["name"]}:{info_plugin["version"]}执行before步骤时失败')
                logging.error(traceback.format_exc())
                del info_plugin['alive']

        self.list_plugins = [info for info in self.list_plugins if info.get('alive', None)]

    def arbiter_around(self, instance, *args, **kwargs) -> bool:
        from flask import request

        result_arbit = []

        for info_plugin in self.list_plugins:
            try:
                response = requests.post(
                    url=info_plugin['arbiter_around'],
                    headers=headers,
                    data=json.dumps({
                        'headers': request.headers,
                        'args': request.args,
                        'data': request.get_json()
                    }),
                    timeout=info_plugin['timeout']
                )
                if response.status_code == 200:
                    result_arbit.append(response.json()['data']['result_arbit'])
                else:
                    result_arbit.append(False)
                    del info_plugin['around']
            except Exception:
                logging.error(traceback.format_exc())
                result_arbit.append(False)
                del info_plugin['around']

        self.list_plugins = [info for info in self.list_plugins if info.get('around', None)]

        return any(result_arbit) if result_arbit else False

    def around(self, instance, *args, **kwargs) -> dict:
        """
        这里其实就相当于为插件在总线之下提供了一个局部变量，供插件之间进行数据共享
        :param instance:
        :param args:
        :param kwargs:
        :return:
        """
        from flask import request
        result_plugin_before = {
            'data_original': {
                'headers': request.headers,
                'args': request.args,
                'data': request.get_json()
            }
        }
        for info_plugin in self.list_plugins:
            try:
                response = requests.post(
                    url=info_plugin['around'],
                    headers=headers,
                    data=json.dumps(result_plugin_before),
                    timeout=info_plugin['timeout']
                )
                if response.status_code == 200:
                    result_plugin_before = response.json()['data']
            except Exception:
                logging.error(traceback.format_exc())

        del result_plugin_before['data_original']

        return result_plugin_before

    def after(self, instance, *args, **kwargs):
        for info_plugin in self.list_plugins:
            try:
                requests.post(
                    url=info_plugin['around'],
                    headers=headers,
                    timeout=info_plugin['timeout']
                )
            except Exception:
                logging.error(traceback.format_exc())

    def after_throwing(self, e, instance, *args, **kwargs) -> dict:
        """
        插件侧面倘若存在异常情况，那么其实作为非主流程，不应当干扰程序的正常运行，输出一下异常信息即可
        :param e:
        :param instance:
        :param args:
        :param kwargs:
        :return:
        """
        logging.error(e)

        return {}
