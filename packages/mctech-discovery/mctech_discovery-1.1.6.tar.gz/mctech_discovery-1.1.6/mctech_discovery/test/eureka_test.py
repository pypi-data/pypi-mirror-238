from __future__ import absolute_import
from ..rpc import rpc
from ..rpc.request_context import PipeRpcInvoker, RpcServiceInfo, RpcInvoker
from ..discovery import discovery_client
import asyncio

discovery_client.start()
configure = discovery_client.load_config()
discovery_client.register()
configure.merge()
########################################################################
result = rpc.post(
    RpcInvoker(path='/page_ocr', body={
                   "from": "page",
                   "type": "subsequent",
                   "image": {
                       "storage": {
                           "product": "drawing-result",
                           "tenantIgnore": True,
                           "key": '1646461686616576/1/nontable.png',
                       },
                       "extraArgs": {
                           "image_transform": {},
                           "return_text_boxes": True
                       }
                   }
               }),
    RpcServiceInfo(service_id='infra-ocr-mxz-service')
)
print(result)
# bind_rpc = rpc.bind(RpcServiceInfo(service_id='sequence-service'))
# result = bind_rpc.stream(
#     PipeRpcInvoker(path='/nexts', method='post',
#                    query={'count': 5}, params={'id': 123456}),
# )

# # print(json.dumps(configure.get_config()))
# print(result)

# ########################################################################
# result = rpc.get(
#     RpcInvoker(path='/cas/supports.do'),
#     RpcServiceInfo(service_id='cas-site')
# )
# print(type(result))
# print(result)

# result = rpc.get(
#     RpcInvoker(path='/cas/supports.do', json=False),
#     RpcServiceInfo(service_id='cas-site')
# )
# print(result)
# print(type(result))


# ########################################################################
# result = asyncio.run(rpc.get_async(
#     RpcInvoker(path='/cas/supports.do'),
#     RpcServiceInfo(service_id='cas-site')
# ))
# print(type(result))
# print(result)

# result = asyncio.run(rpc.get_async(
#     RpcInvoker(path='/cas/supports.do', json=False),
#     RpcServiceInfo(service_id='cas-site')
# ))
# print(result)
# print(type(result))


# ########################################################################
# try:
#     result = rpc.post(
#         RpcInvoker(path='/nexts',
#                    query={'count': -5}),
#         RpcServiceInfo(service_id='sequence-service')
#     )
# except Exception as ex:
#     print(ex)
