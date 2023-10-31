import importlib
import os
import traceback

from Flask_FrameMVC.core.Basics import BasicConfig, BeforeServlet, BackServlet, BasicInteraction, OutContextBeforeServlet, OutContextBackServlet
from Flask_FrameMVC.ConfigContainer import configs, routers, servlets_before, servlets_back, servlets_before_out_context, servlets_back_out_context


def scan_config(directory_path):
    configs_custom = []
    for r, d, filenames in os.walk(directory_path):
        if 'mvc' not in r or 'config' not in r:
            continue
        for filename in filenames:
            if filename == '__init__.py' or not filename.endswith('.py'):
                continue

            try:
                module = importlib.machinery.SourceFileLoader(
                    filename.replace(',py', ''), os.path.join(r, filename)
                ).load_module()
                class_imported = getattr(module, filename.replace('.py', ''))
                if issubclass(class_imported, BasicConfig):
                    configs_custom.append(class_imported)
            except Exception:
                print(traceback.format_exc())
    configs_custom.sort(key=lambda x: x.sort)
    configs.extend(configs_custom)


def scan_servlet(directory_path):
    for r, d, filenames in os.walk(directory_path):
        if 'mvc' not in r or 'servlet' not in r:
            continue

        for filename in filenames:
            if filename == '__init__.py' or not filename.endswith('.py'):
                continue

            try:
                module = importlib.machinery.SourceFileLoader(
                    filename.replace(',py', ''), os.path.join(r, filename)
                ).load_module()

                class_imported = getattr(module, filename.replace('.py', ''))
                if issubclass(class_imported, BeforeServlet):
                    servlets_before.append(class_imported())
                if issubclass(class_imported, BackServlet):
                    servlets_back.append(class_imported())

            except Exception:
                print(traceback.format_exc())

        servlets_before.sort(key=lambda x: x.sort)
        servlets_back.sort(key=lambda x: x.sort)


def scan_servlet_out_context(directory_path):
    for r, d, filenames in os.walk(directory_path):
        if 'mvc' not in r or 'servlet' not in r:
            continue

        for filename in filenames:
            if filename == '__init__.py' or not filename.endswith('.py'):
                continue

            try:
                module = importlib.machinery.SourceFileLoader(
                    filename.replace(',py', ''), os.path.join(r, filename)
                ).load_module()

                class_imported = getattr(module, filename.replace('.py', ''))
                if issubclass(class_imported, OutContextBeforeServlet):
                    servlets_before_out_context.append(class_imported())
                if issubclass(class_imported, OutContextBackServlet):
                    servlets_back_out_context.append(class_imported())

            except Exception:
                print(traceback.format_exc())

        servlets_before_out_context.sort(key=lambda x: x.sort)
        servlets_back_out_context.sort(key=lambda x: x.sort)


def scan_router(directory_path):
    for r, d, filenames in os.walk(directory_path):
        if 'mvc' not in r or 'router' not in r:
            continue

        for filename in filenames:
            if filename == '__init__.py' or not filename.endswith('.py'):
                continue

            try:
                module = importlib.machinery.SourceFileLoader(
                    filename.replace(',py', ''), os.path.join(r, filename)
                ).load_module()

                class_imported = getattr(module, filename.replace('.py', ''))
                if issubclass(class_imported, BasicInteraction):
                    routers.append(class_imported)

            except Exception:
                print(traceback.format_exc())
