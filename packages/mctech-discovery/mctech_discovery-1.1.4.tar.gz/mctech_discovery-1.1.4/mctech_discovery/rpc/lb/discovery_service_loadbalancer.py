from __future__ import absolute_import
from log4py import logging
from ...discovery import discovery_client
from .loadbalancer import LoadBalancer
from ..request_context import InternalRequestContext, RpcInvoker, \
    RpcServiceInfo, EndPoint
from ..ep.ep_request import EndPointRequest
from ..rule.simple_rule import SimpleRule

log = logging.getLogger('python.cloud.rpc.loadbalancer')


class DiscoveryServiceLoadBalancer (LoadBalancer):
    '''
    通过Eureka服务动态获取可用的服务端地址的实现
    '''

    def __init__(self, service_id, app_name):
        super().__init__()
        self.service_id = service_id
        self.app_name = app_name
        self._rule = SimpleRule(service_id, discovery_client.client)

    def check_alive(self) -> bool:
        # 重新计算各节点权重值
        try:
            if self._rule.check_alive():
                self._rule.compute()
                return True
        except Exception as err:
            log.error('Error calculating server weights', err)

        # 目标服务例不在线或者计算权重失败时都返回false
        return False

    def chooseOne(self) -> EndPoint:
        inst = self._rule.choose_server()
        return inst

    def create_context(self,
                       invoker: RpcInvoker,
                       service: RpcServiceInfo) -> InternalRequestContext:
        return InternalRequestContext(invoker, service, self.app_name)

    async def execute(self, req: EndPointRequest):
        ep = self._rule.choose_server()
        result_data = await req.execute(ep)
        return result_data

    async def stream(self, req: EndPointRequest):
        ep = self._rule.choose_server()
        result_stream = await req.stream(ep)
        return result_stream

    def ws(self, req: EndPointRequest):
        ep = self._rule.choose_server()
        conn = req.ws(ep)
        return conn
