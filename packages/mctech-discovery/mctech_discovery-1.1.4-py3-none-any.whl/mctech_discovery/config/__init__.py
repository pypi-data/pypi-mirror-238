from __future__ import absolute_import
from log4py import Logger
import os
import sys
from typing import Dict
from ._configure import Configure


def _load_env_params(params: Dict[str, str]):
    '''
    初始化环境变量的配置
    '''
    for envKey, value in os.environ.items():
        if envKey.find('NODE_') == 0:
            key = envKey[envKey.find('_') + 1:].lower().replace('_', '.')
            params[key] = value


def _load_cmd_params(params: Dict[str, str]):
    '''
    初始化命令行的配置参数
    '''
    for arg in sys.argv:
        if arg.find('--') == 0:
            info = arg[2:].split('=')
            if len(info) == 2:
                [key, value] = info
                params[key.lower()] = value


_params: Dict[str, str] = {}
# 获取环境变量
_load_env_params(_params)
# 获取命令行参数，可以保证命令行参数优先于环境变量
_load_cmd_params(_params)

Logger.set_level('INFO')

configure = Configure(_params)
