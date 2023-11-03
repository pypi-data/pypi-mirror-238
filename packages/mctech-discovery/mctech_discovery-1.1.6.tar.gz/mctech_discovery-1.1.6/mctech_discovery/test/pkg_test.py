from mctech_discovery.rpc import rpc
from mctech_discovery.rpc.request_context import RpcInvoker, RpcServiceInfo
from mctech_discovery.discovery import discovery_client as client


client.start()
configure = client.load_config()
configure.merge()
# result = rpc.post(RpcInvoker(path='/nexts',
#                   method = "get", query={'count': 5}, params={'id': 123456}),
#                   RpcServiceInfo(service_id='sequence-service'))
bind_rpc = rpc.bind(RpcServiceInfo(service_id='sequence-service'))
result = bind_rpc.post(
    RpcInvoker(path='/nexts', method="get",
               query={'count': 5}, params={'id': 123456}),
)
print(result)
