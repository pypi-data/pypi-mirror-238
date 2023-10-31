import importlib
from typing import Tuple, Any, Dict

from shortuuid import uuid

from Flask_FrameMVC.core.Basics.controller import BasicController
from Flask_FrameMVC.core.Exception.Exceptions import BootException


def factory_cls_controller(func_test, path_parameter: str):
    """
    动态创建controller类，并将其get方法替换为MethodTestSide.funcs中的方法
    :param path_parameter: 路径所指必须是py文件
    :param func_test: 待测函数/方法
    :return:
    """
    if not path_parameter.endswith('.py'):
        raise BootException('测试参数文件格式不正确')

    module = importlib.machinery.SourceFileLoader(
        path_parameter.split('/')[-1].replace(',py', ''), path_parameter
    ).load_module()

    args: Tuple[Any, ...] = getattr(module, 'args', None)
    kwargs: Dict[str, Any] = getattr(module, 'kwargs', None)

    if args is None and kwargs is None:
        raise BootException('测试参数文件没有参数容器args/kwargs')
    elif args is not None and not isinstance(args, tuple):
        raise BootException('测试参数文件中参数容器args当前并非数组')
    elif kwargs is not None and not isinstance(kwargs, dict):
        raise BootException('测试参数文件中参数容器kwargs当前并非字典')

    def get(self):

        if args is not None and kwargs is None:
            return func_test(*args)
        elif args is None and kwargs is not None:
            return func_test(**kwargs)
        else:
            return func_test(*args, **kwargs)

    cls_controller = type(uuid(), (BasicController,), {'get': get})

    return cls_controller


class HiddenTestController(BasicController):

    def get(self):

        return {
            "code": 200,
            "message": '这是一个隐藏接口'
        }
