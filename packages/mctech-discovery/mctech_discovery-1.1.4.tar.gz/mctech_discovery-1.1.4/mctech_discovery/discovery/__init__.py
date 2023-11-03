from __future__ import absolute_import
import socket
import netifaces
from log4py import logging
from .local_discovery_client import LocalDiscoveryClient
from .eureka_discovery_client import EurekaDiscoveryClient
from ..config import configure

log = logging.getLogger('python.eureka.discoveryClient')


def getIPAdress():
    '''
    获取本机ip
    '''

    result = []
    for iface in netifaces.interfaces():
        alias = netifaces.ifaddresses(iface)
        ipv4 = alias.get(netifaces.AF_INET)
        if ipv4 is None:
            continue
        for addr_info in ipv4:
            address = addr_info["addr"]
            if address == '127.0.0.1':
                continue
            result.append(addr_info["addr"])

    if len(result) == 0:
        raise RuntimeError('未找到合适的ipv4地址')

    if len(result) > 1:
        log.warning('找到多个符合条件的ipv4地址: %s' % result)

    selected_address = result[0]
    log.info('当前使用的ip地址: ' + selected_address)

    return selected_address


def __create_discovery_client():
    eurekaConfig = configure.get_config('eureka', {'enabled': True})
    DiscoveryClientCls = EurekaDiscoveryClient if eurekaConfig["enabled"] \
        else LocalDiscoveryClient

    ipAddress = getIPAdress()
    hostName = socket.gethostname()
    return DiscoveryClientCls(ipAddress, hostName)


discovery_client = __create_discovery_client()
