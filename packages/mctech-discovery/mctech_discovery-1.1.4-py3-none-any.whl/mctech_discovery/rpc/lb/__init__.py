from __future__ import absolute_import
from typing import Dict
from urllib.parse import urlparse
from threading import Timer
from ...discovery import discovery_client
from ...config import configure
from ..request_context import RpcServiceInfo, EndPoint
from .direct_loadbalancer import DirectLoadBalancer
from .discovery_service_loadbalancer import DiscoveryServiceLoadBalancer
from .local_service_loadabalancer import LocalServiceLoadBalancer
from .loadbalancer import LoadBalancer
from .retry_loadbalancer import RetryLoadBalancer
from mctech_actuator.health import manager

# gateway = GatewayLoadBalancer()
direct = DirectLoadBalancer()


load_balance_cache: Dict[str, LoadBalancer] = {}
local_service: Dict[str, str] = {}
dependencies: Dict[str, bool] = {}


def _metric_endpoint(*, request):
    return [v for v in load_balance_cache.keys()]


manager.add_metric({
    # 相对于/actuator/metrics的路径，必须以'/'开头
    'path': '/dependencies',
    'endpoint': _metric_endpoint
})

CHECK_ALIVE_INTERVAL = 5

# 定时检查目标服务的信息是否还有效，如果不存在了，则会移除


def print_time():
    invalidates = []
    for serviceId, lb in load_balance_cache.items():
        if not lb.check_alive():
            invalidates.append(serviceId)

    # 存在失效的服务，从缓存中移除
    if len(invalidates) > 0:
        for service_id in invalidates:
            del load_balance_cache[service_id]


# 指定1秒后执行print_time函数
t = Timer(CHECK_ALIVE_INTERVAL, print_time)
t.start()


app_name: str = None


def _load_config():
    config = configure.get_config('mctech.rpc.service')

    for service_id, service_url in config:
        result = urlparse(service_url)
        local_service[service_id] = EndPoint(
            id=service_id,
            host=result['hostname'],
            port=result.get('port')
        )


def create(retry: int, service: RpcServiceInfo) -> LoadBalancer:

    if not app_name:
        _load_config()

    retry = retry or 0
    rpc_type = service.rpc_type if service.rpc_type else 'internal'

    # lb: LoadBalancer
    # if type == 'gateway':
    #   lb = gateway
    # el
    if rpc_type == 'internal':
        # 配置的是servicieId
        lb = get_internal_loadbalancer(service.service_id)
    else:
        raise RuntimeError('不支持的调用方式')

    if retry > 0:
        lb = RetryLoadBalancer(lb)
    return lb


def get_internal_loadbalancer(service_id: str) -> LoadBalancer:
    if not service_id:
        lb = direct
    else:
        lb = load_balance_cache.get(service_id)
        if not lb:
            inst = local_service.get(service_id)
            if inst:
                lb = LocalServiceLoadBalancer(inst, app_name)
            elif not discovery_client.isLocal:
                lb = DiscoveryServiceLoadBalancer(service_id, app_name)
            elif not inst:
                raise RuntimeError(
                    "本地调用配置中未找到service_id为: '%s'的服务" % service_id
                )

            load_balance_cache[service_id] = lb
            dependencies[service_id] = True
    return lb
