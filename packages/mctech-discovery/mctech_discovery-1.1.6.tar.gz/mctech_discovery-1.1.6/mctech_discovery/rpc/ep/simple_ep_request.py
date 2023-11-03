from __future__ import absolute_import
from .ep_request import EndPointRequest
from ..request_context import EndPoint
from .internal_rpc import execute as rpc_execute, \
    stream as rpc_stream, ws as rpc_ws


class SimpleEndPointRequest (EndPointRequest):
    async def execute(self, ep: EndPoint):
        resultData = await rpc_execute(self.context, ep)
        return resultData

    async def stream(self, ep: EndPoint):
        '''
        :return Awaitable[httpx.Response]
        '''
        resultStream = await rpc_stream(self.context, ep)
        return resultStream

    def ws(self, ep: EndPoint):
        '''
        :return Stream
        '''
        conn = rpc_ws(self.context, ep)
        return conn
