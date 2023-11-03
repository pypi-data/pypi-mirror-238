from __future__ import absolute_import
from py_eureka_client.eureka_client import EurekaClient
import sys
import os
import time
import posixpath
import asyncio

from log4py import logging
from typing import Dict
from urllib import parse
from ..config import configure
from ..lifecycle import lifecycle

sys.path.append('../')
log = logging.getLogger('python.discovery.eurekaDiscoverClient')

event_loop = asyncio . get_event_loop()  # 创建一个默认的事件循环


def _create_client_config(localAddress: str,
                          hostName: str, remoteLoaded: bool):
    '''
    创建eureka客户端配置信息
    :param localAddress
    :param hostName
    :param remoteLoaded
    '''
    info = configure.get_app_info()

    # 准备注册信息
    name = info.get("name")
    port = info.get("port")

    defaultConfig = {
        'perferIpAddress': True,
        'registerEureka': True,
        'client': {
            'serverUrls': 'http://localhost:8761/eureka/'
        }
    }

    config = configure.get_config('eureka', defaultConfig)
    ipAddress = config.get("ipAddress", localAddress)
    servers = resolve_eureka_servers(config["client"].get("serverUrls"))
    # 启用了远程配置且未加载远程配置时，不注册到eureka上
    registerEureka = False if not remoteLoaded else config["registerEureka"]

    management = configure.get_config('management')
    homePageUrl = "http://%s:%s" % (ipAddress, port)
    preferIpAddress = True if not config.__contains__(
        "preferIpAddress") else config["preferIpAddress"]
    return {
        'instance': {
            'instanceId': "%s:%s:%d" % (hostName, name, port),
            'hostName': ipAddress if preferIpAddress else hostName,
            'app': name,
            'ipAddr': ipAddress,
            'port': port,
            'homePageUrl': homePageUrl,
            'statusPageUrl': parse.urljoin(
                homePageUrl,
                posixpath.join(management.get("contextPath"), 'info')),
            'healthCheckUrl': parse.urljoin(
                homePageUrl,
                posixpath.join(management.get("contextPath"), '/health')),
            'vipAddress': os.environ.get('SERVICE_VIP_ADDRESS', name),
            'metadata': {
                'management.context-path': management.get("contextPath")
            },
            'leaseInfo': {
                'renewalIntervalInSecs': None if not config.get("instance")
                else config["instance"]["renewalIntervalInSecs"],
                'durationInSecs': None if not config.get("instance")
                else config["instance"]["durationInSecs"]
            }
        },
        'eureka': {
            'fetchRegistry': True,
            'heartbeatInterval': 5000,
            'registryFetchInterval': 15000,
            'registerWithEureka': registerEureka,
            'preferIpAddress': preferIpAddress,
            'serviceUrls': servers
        }
    }


def resolve_eureka_servers(serverUrls: str):
    '''
    格式化注册中心地址，地址后统一加上/app/
    :param serverUrls 注册中心列表
    '''

    # 在当前版本下不需要处理，使用的eureka包里会自动处理
    return serverUrls


def _convert_to_eureka_args(config: dict):
    instance = config["instance"]
    renewalIntervalInSecs = instance["leaseInfo"]["renewalIntervalInSecs"]
    eureka = config["eureka"]
    instance = config["instance"]
    renewalIntervalInSecs = instance["leaseInfo"]["renewalIntervalInSecs"]
    return {
        'eureka_server': eureka["serviceUrls"],
        'app_name': instance["app"],
        'instance_id': instance["instanceId"],
        'instance_host': instance["hostName"],
        'instance_ip': instance["ipAddr"],
        'instance_port': instance["port"],
        'renewal_interval_in_secs': renewalIntervalInSecs,
        'home_page_url': instance["homePageUrl"],
        'status_page_url': instance["statusPageUrl"],
        'health_check_url': instance["healthCheckUrl"],
        'vip_adr': instance["vipAddress"],
        'should_register': eureka["registerWithEureka"],
        'metadata': instance["metadata"]
    }


class EurekaDiscoveryClient():
    '''
    服务发现客户端, 注册到发现服务器
    '''

    def __init__(self, local_address: str, host_name: str):
        self._local_address = local_address
        self._host_name = host_name

        # 创建client实例
        self._config = _create_client_config(local_address, host_name, False)
        kwargs = _convert_to_eureka_args(self._config)
        self._client = EurekaClient(**kwargs)

    @property
    def client(self) -> EurekaClient:
        return self._client

    @property
    def local_instance(self):
        return self._config["instance"]

    @property
    def isLocal(self):
        return False

    def start(self):
        '''
        启动客户端
        '''

        self._start(self._client)

    def _start(self, client: EurekaClient = None):
        if not client:
            client = self._client

        lifecycle.before_start()
        event_loop.run_until_complete(client.start())
        servers = self._config['eureka']['serviceUrls']
        if client.should_register:
            log.info("发布到注册中心: %s" % servers)
        else:
            log.info("连接到注册中心: %s" % servers)

        oldClient = self._client
        # 切换为新的client
        self._client = client

        if oldClient != client:
            event_loop.run_until_complete(oldClient.stop())

    def register(self):
        # 根据需要把当前应用注册到服务中心
        newConfig = _create_client_config(
            self._local_address, self._host_name, True)
        eureka = newConfig["eureka"]
        should_register_to_eureka = eureka["registerWithEureka"]
        if not should_register_to_eureka:
            # 不需要注册到服务中心
            return

        kwargs = _convert_to_eureka_args(newConfig)
        eureka = EurekaClient(**kwargs)
        self._start(eureka)
        self._config = newConfig
        # 等待2秒
        time.sleep(2)

    def unregister(self):
        event_loop.run_until_complete(self._client.stop())

        # 在注册中心取消当前服务注册后，延迟一个`registryFetchInterval`周期结束
        # 防止服务调用端在没有更新注册信息前仍然把请求发送到当前实例中
        delayMs = self._config.eureka.registryFetchInterval + 5000
        time.sleep(delayMs)

    def load_config(self):
        defaultConfig = {
            'id': 'config-server',
            'enabled': True
        }

        config_server = configure.get_config('config.server', defaultConfig)
        if not config_server["enabled"]:
            return configure

        appInfo = configure.get_app_info()
        name = appInfo.get("name", "")
        active_profiles = configure.active_profiles
        if not active_profiles:
            active_profiles = "default"

        assert len(name) > 0, "配置文件中未获取到'name'的值"

        remote_path = "/%s/%s/" % (name, active_profiles)

        # 远程服务器上配置文件的路径
        service_id = config_server["id"]
        assert service_id, "配置文件中未获取到'config.server.id'的值"

        # 等待1秒，避免出现未初始化完全的问题
        time.sleep(1)
        future = self.client.do_service(
            config_server["id"],
            remote_path, return_type="json")
        remote_config = event_loop.run_until_complete(future)
        if remote_config:
            log.info("从配置中心获取到配置信息. file: %s" % remote_path)
        else:
            log.info("远程服务器未发现配置文件. file: %s" % remote_path)

        property_sources: list = remote_config["propertySources"]
        # 返回的列表是按profilesy优先级高的在前面，合并的时候需要按优先级低的先合并
        # 所以这里需要取反
        property_sources.reverse()
        for s in property_sources:
            name = s["name"]
            source = s["source"]
            pathname = parse.urlparse(name).path
            filename: str = posixpath.basename(pathname).replace('.yml', '')
            profile = 'default'
            if filename != name and filename != 'appliction':
                lastIndex = filename.rfind('-')
                if lastIndex > 0:
                    profile = filename[lastIndex + 1:]

            params = _resolve_params(source)
            configure.use(source, name, profile, params)
        return configure


def _resolve_params(source: Dict[str, str]):
    params: Dict[str, str] = {}
    keys = list(source.keys())
    for key in keys:
        segments = key.split('.')
        prefix = segments[0]
        if prefix == 'params':
            segments.pop(0)
            param_name = '.'.join(segments)
            params[param_name] = source[key]
            source.pop(key)
    return params
