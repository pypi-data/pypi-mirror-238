import importlib
import inspect
import os
import traceback

from functools import partial

from Flask_FrameMVC.core.Basics.interaction import BasicHttpRouter
from Flask_FrameMVC.side.TestSide import MethodTestSide, FunctionTestSide
from Flask_FrameMVC.default.controller.TestHttpControllerFactory import factory_cls_controller, HiddenTestController


def scan_case(directory_path) -> dict:

    for r, d, filenames in os.walk(directory_path):
        if 'mvc' not in r or 'service' not in r:
            continue

        for filename in filenames:
            if filename == '__init__.py' or not filename.endswith('.py'):
                continue

            try:
                module = importlib.machinery.SourceFileLoader(
                    filename.replace(',py', ''), os.path.join(r, filename)
                ).load_module()

                if MethodTestSide not in [tup[1] for tup in inspect.getmembers(module)] and FunctionTestSide not in [tup[1] for tup in inspect.getmembers(module)]:
                    continue

                # 将所有的对象都实例化并使用方法一次，再使用一次模块中所适配的函数，这样一来MethodTestSide的funcs中就包含了文件中所有被修饰的方法并变形成功
                instances = [
                    cls[1](*cls[1].test_args) for cls in inspect.getmembers(module) if inspect.isclass(cls[1]) and any(
                        value for value in cls[1].__dict__.values() if isinstance(value, MethodTestSide)
                    )
                ]
                methods = [getattr(instance, m) for instance in instances for m in dir(instance) if
                           isinstance(getattr(instance, m), partial)]
                functions = [func for func in inspect.getmembers(module) if inspect.isfunction(func)]

            except Exception:
                print(traceback.format_exc())

    return {
        '/' + key: factory_cls_controller(
            value, directory_path + f'resources/test/{key}.py'
        ) for key, value in MethodTestSide.funcs.items()
    }


class TestHttpRouter(BasicHttpRouter):

    def register(self):

        self.dict_resource = {
            '/HiDdEn': HiddenTestController
        }
        self.dict_resource.update(scan_case(self.app.path_project))
        self.name_bp = 'DefaultTestHttpRouter'
        self.url_prefix = '/sys/side/test'
