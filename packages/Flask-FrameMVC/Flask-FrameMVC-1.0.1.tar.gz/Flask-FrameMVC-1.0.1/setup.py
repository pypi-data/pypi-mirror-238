"""
- author:bichuantao
- creation time:2023.10.29
"""

import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# you need to change all these
VERSION = '1.0.1'
DESCRIPTION = ' a flask frame mvc both Win and Mac '
LONG_DESCRIPTION = 'Flask-FrameMVC is a flask boot framework both Win and Mac'

setup(
    name="Flask-FrameMVC",
    version=VERSION,
    author="bichuantao",
    author_email='17826066203@163.com',
    url='https://github.com/ababbabbb/programme/tree/master/topics/backend/netapis/netapi_flask/flask_boot',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    license='MIT',
    install_requires=[
        'flasgger',
        'Flask',
        'Flask-RESTful',
        'Flask-SocketIO',
        'Flask-SQLAlchemy',
        'SQLAlchemy'
    ],
    keywords=['python', 'flask', 'mvc', 'framework'],
    classifiers=[
        # 开发状态
        'Development Status :: 3 - Alpha',

        # 开发的目标用户
        'Intended Audience :: Developers',

        # 主题
        'Topic :: Software Development :: Build Tools',

        # 许可证信息
        'License :: OSI Approved :: MIT License',

        # 目标 Python 版本
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)