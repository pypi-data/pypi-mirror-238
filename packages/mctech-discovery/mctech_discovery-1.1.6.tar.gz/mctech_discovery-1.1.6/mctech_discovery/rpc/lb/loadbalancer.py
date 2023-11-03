from __future__ import absolute_import

from abc import ABC, abstractmethod, abstractproperty
from ..request_context import AbstractInvoker, RpcServiceInfo, \
    RequestContext, EndPoint
from ..ep.ep_request import EndPointRequest


class LoadBalancer(ABC):
    @abstractmethod
    def create_context(self,
                       invoker: AbstractInvoker,
                       service: RpcServiceInfo) -> RequestContext:
        pass

    @abstractproperty
    def check_alive() -> bool:
        pass

    @abstractmethod
    def chooseOne(self) -> EndPoint:
        return None

    def request(self, method: str, req: EndPointRequest):
        if method == 'execute':
            return self.execute(req)
        elif method == 'stream':
            return self.stream(req)
        elif method == 'ws':
            return self.ws(req)  # 底层创建websocket用的是同步方法，当前返回值会转换成异步调用的包装
        raise RuntimeError('不支持的方法:' + method)

    @abstractmethod
    async def execute(self, req: EndPointRequest):
        pass

    @abstractmethod
    async def stream(self, req: EndPointRequest):
        pass

    @abstractmethod
    def ws(self, req: EndPointRequest):
        '''
        :return websocket.WebSocket
        '''
        pass
