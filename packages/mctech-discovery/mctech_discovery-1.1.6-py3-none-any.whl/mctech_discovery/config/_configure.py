from __future__ import absolute_import
import os
import sys
from typing import Dict, Any
from .config_merger import config_merge, process_source, \
    TypedList, resolve_params
from .config_value import SecurityObject
from . import yaml_loader as loader
import json

# 参数配置及获取结果规则表
config_source_info: Dict[str, Any] = {}


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SecurityObject):
            return obj.toJSON()

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def _get_config_base_dir(params: Dict[str, str]):
    dir_name = os.path.dirname(sys.argv[0])
    if not os.path.exists(os.path.join(dir_name, 'bootstrap.yml')):
        dir_name = params.pop('config.dir',  sys.path[0])
    return dir_name


def _deep_copy_property(target: Dict[str, Any], source: Dict[str, Any]):
    for name, value in source.items():
        # 只有数组或叶子节点的简单值才会对应着来自不同profile里的值
        # 非叶子结点只是一个连接叶子节点的桥梁，不会产生多个值
        if isinstance(value, list):
            union: TypedList = value
            if union.item_type != "array":
                # 非数组，取第一项的值，直接覆盖
                value = union[0].get("value")
            else:
                # 数组值
                v = []
                for i in range(0, len(union)):
                    arr = union[i].get("value")
                    v.extend(arr)
                value = v
        else:
            if isinstance(value, Dict):
                new_value: Dict[str, Any] = {}
                target[name] = new_value
                _deep_copy_property(new_value, value)
                value = new_value

        target[name] = value


def _create_actual_config():
    # 生成一个合并后的配置
    # 生成代理对象
    config: Dict[str, Any] = {}
    _deep_copy_property(config, config_source_info)
    return config


class Configure():
    def __init__(self, params: Dict[str, str]):
        self.params = params
        # 内置在yaml文件内部的参数 $(param这样的格式)
        self.internal_params: Dict[str, Any] = {}
        self._profile_map: Dict[str, Any] = {}
        self._active_profiles = ""

        # 加载默认的配置
        self.use(
            {
                "application": {"port": 8080, "profiles": {"active": ""}},
                "management": {"contextPath": "/actuator"}
            },
            "default-internal",
            "default"
        )

        # 加载bootstrap.yml文件
        self._config_base_dir = _get_config_base_dir(params)
        self._load_config_from_local(params)
        # 合并"default"配置的默认值
        cfg_list = self._profile_map.get("default")
        if cfg_list and len(cfg_list):
            for config in cfg_list:
                config_merge(target=config_source_info,
                             source=config.get("source"),
                             type=config.get("name"))
                config["merged"] = True

                # 从"default"配置上提取激活的profiles
                active_profiles = _get_config_segment(
                    config.get("source"),
                    "application.profiles.active"
                )
                if active_profiles:
                    if self._active_profiles:
                        self._active_profiles = self._active_profiles + \
                            "," + active_profiles
                    else:
                        self._active_profiles = active_profiles
        self._config = _create_actual_config()

    def use(self, source, name: str, profile: str,
            params: Dict[str, str] = {}):
        '''
        加载从其它来源获取到的配置

        :param source
        :param name: 用于追跟踪配置段来源的标识
        :param profile:
        :param params: 内部引用的参数集合
        '''
        source_list = self._profile_map.get(profile)
        if source_list is None:
            source_list = []
            self._profile_map[profile] = source_list

        # 合并参数
        resolve_params(self.internal_params, params)
        # 替换处理内置参数
        source_json = process_source(source, self.internal_params)

        source_list.append({'name': name, 'source': source_json})

    def merge(self):
        if (self._active_profiles):
            active_profile_names = self._active_profiles.split(",")
            # 加载远程服配置中的"defaualt"配置
            active_profile_names.insert(0, "default")
            # 根据激活的profiles加载其它的配置
            for name in active_profile_names:
                cfg_list = self._profile_map.get(name)
                if (cfg_list is None or len(cfg_list) == 0):
                    continue

                for config in cfg_list:
                    if config.get('merged'):
                        # 之前已经合并过，不再合并
                        continue
                    config_merge(config_source_info,
                                 config["source"], config["name"])
                    config['merged'] = True

        self._config = _create_actual_config()

    @property
    def active_profiles(self):
        return self._active_profiles

    def get_config_source_info(self):
        return config_source_info

    def get_app_info(self):
        app = self._config.get("application")
        return {
            "name": app.get("name"),
            "port": app.get("port"),
            "env": app.get("env"),
            "cloudName": app.get("cloudName")
        }

    def get_config(self, prefix="", config: Dict[str, Any] = None):
        '''
        获取指定配置段的配置值
        :param prefix 配置对象中路径前缀
        :param config 配置的默认值
        '''
        if config is None:
            config = {}

        if (len(prefix) == 0):
            v = self._merge(config, self._config)
            return v

        c = _get_config_segment(self._config, prefix)
        return self._merge(config, c)

    def _merge(self, target: Dict[str, Any], source: Dict[str, Any]):
        if (source is None):
            return target

        for name, source_value in source.items():
            if (source_value is None):
                continue

            # json对象
            if isinstance(source_value, Dict):
                target_value = target.get(name)
                if (target_value is None):
                    target_value: Dict[str, Any] = {}
                    target[name] = target_value
                elif not isinstance(target_value, Dict):
                    error_msg = "配置段类型不匹配. source: %s, target: %s" % (
                        source_value, target_value)
                    raise RuntimeError(error_msg)
                self._merge(target_value, source_value)
            else:
                # 其它值类型
                target[name] = source_value
        return target

    # / **
    #  * @ param {Map < string, string >} params
    #  * /
    def _load_config_from_local(self, params):
        config_names = ["bootstrap", "individual"]
        for name in config_names:
            config_file = os.path.join(self._config_base_dir, name + ".yml")
            abs_file = os.path.abspath(config_file)
            if (not os.path.exists(abs_file)):
                continue
            # 把yaml文件解析为一个或多个配置对象
            profile_configs = loader.get_yaml_objects(config_file, params)
            # 把各个配置对象按profiles -> config的映射方式存到map中
            for cfg in profile_configs:
                profile_name = cfg.pop("application.profiles", "default")
                params: Dict[str, str] = cfg.pop("params", {})
                self.use(cfg, profile_name + '-local', profile_name, params)


def _get_config_segment(config: Dict[str, Any], prefix: str):
    c = config
    segments = prefix.split('.')
    for i in range(0, len(segments)):
        segment = segments[i]
        c = c.get(segment)
        if (c is None):
            break
    return c
