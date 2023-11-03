from __future__ import absolute_import

import abc
import os
import py_eureka_client.eureka_client as eureka_client

from ..request_context import EndPoint

k8s = 'KUBERNETES_SERVICE_HOST' in os.environ


class AbstractRule:
    def __init__(self, app_id: str, eureka: eureka_client.EurekaClient):
        self._app_id = app_id
        self._app_id_upper = app_id.upper()
        self._eureka = eureka

    def choose_server(self) -> EndPoint:
        inst = self._choose()
        if not inst:
            raise RuntimeError('没有可用的服务: ' + self._app_id)

        if k8s and inst.vipAddress.endswith('.svc'):
            return EndPoint(id=inst.instanceId,
                            host=inst.vipAddress,
                            port=inst.port.port)

        # 使用EurekaClient内部的调用算法
        return None

    @abc.abstractmethod
    def _choose(self) -> eureka_client.Instance:
        pass

    def compute(self):
        pass

    def record_stats(self, server_id: str, responseTime: int):
        pass
