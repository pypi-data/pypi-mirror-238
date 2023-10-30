# -*- coding: utf-8 -*-
"""
@Author : zhang.yonggang
@File   : setup.py.py
@Project: pydlt_plus
@Time   : 2023-10-26 08:28:01
@Desc   : The file is ...
@Version: v1.2.0
"""
from setuptools import setup, find_packages


def parse_requirements(filename):
    """ load requirements from a pip requirements file. (replacing from pip.req import parse_requirements)"""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


reqs = parse_requirements('requirements.txt')

setup(
    name='nost_util_tools',
    version='1.0.0',
    author='Arthur Nostmabole Zhang',
    author_email='nostmabole@sina.com',
    description='This is a collection of tools that includes encapsulations of some commonly '
                'used utilities such as file and folder operations, common database operations, '
                'image processing, and network connectivity.',
    long_description='''
                        This is a collection of tools that includes encapsulations of some commonly 
                        used utilities such as file and folder operations, common database operations, 
                        image processing, and network connectivity.
                    ''',
    url='https://gitee.com/nostmabole/py_util_tools',
    license='Apache License 2.0',
    packages=find_packages(exclude=['cover', 'playground', 'tests', 'dist', 'venv']),
    install_requires=reqs,
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
