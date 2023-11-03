from __future__ import absolute_import
from abc import ABC, abstractmethod
from ..request_context import RequestContext, EndPoint


class EndPointRequest(ABC):
    def __init__(self, context: RequestContext):
        self.context = context

    @abstractmethod
    async def execute(self, ep: EndPoint):
        '''
        :return Awaitable[Any]
        '''
        pass

    @abstractmethod
    async def stream(self, ep: EndPoint):
        '''
        :return Awaitable[httpx.Response]
        '''
        pass

    @abstractmethod
    def ws(self, ep: EndPoint):
        '''
        :return websocket.WebSocket
        '''
        pass
