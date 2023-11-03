from __future__ import absolute_import
from .loadbalancer import LoadBalancer
from ..request_context import RpcInvoker, RpcServiceInfo, \
    EndPoint, RequestContext
from ..ep.ep_request import EndPointRequest


class RetryLoadBalancer(LoadBalancer):

    def __init__(self, lb: LoadBalancer):
        super().__init__()
        self._lb = lb

    def check_alive(self):
        return self._lb.check_alive()

    def chooseOne(self) -> EndPoint:
        return self._lb.chooseOne()

    def create_context(self,
                       invoker: RpcInvoker,
                       service: RpcServiceInfo) -> RequestContext:
        return self._lb.create_context(invoker, service)

    async def execute(self, req: EndPointRequest):
        result_data = await self._lb.execute(req)
        return result_data

    async def stream(self, req: EndPointRequest):
        result_stream = await self._lb.stream(req)
        return result_stream

    def ws(self, req: EndPointRequest):
        conn = self._lb.ws(req)
        return conn
