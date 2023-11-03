from __future__ import absolute_import
from .loadbalancer import LoadBalancer
from ..request_context import InternalRequestContext, RpcInvoker, \
    RpcServiceInfo, EndPoint
from ..ep.ep_request import EndPointRequest


class LocalServiceLoadBalancer (LoadBalancer):
    '''
    显示指定了调用的目标地址的LoadBalancer实现方式
    '''

    def __init__(self, inst: EndPoint, app_name):
        super().__init__()
        self._inst = inst
        self.app_name = app_name

    def check_alive(self):
        return True

    def chooseOne(self) -> EndPoint:
        return self._inst

    def create_context(self,
                       invoker: RpcInvoker,
                       service: RpcServiceInfo) -> InternalRequestContext:
        return InternalRequestContext(invoker, service, self.app_name)

    async def execute(self, req: EndPointRequest):
        result_data = await req.execute(self._inst)
        return result_data

    async def stream(self, req: EndPointRequest):
        result_stream = await req.stream(self._inst)
        return result_stream

    def ws(self, req: EndPointRequest):
        conn = req.ws(self._inst)
        return conn
