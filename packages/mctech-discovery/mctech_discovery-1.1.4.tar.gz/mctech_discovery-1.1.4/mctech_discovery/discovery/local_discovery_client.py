from __future__ import absolute_import
from ..config import configure


class LocalDiscoveryClient():
    def __init__(self, localAddress: str, hostName: str):
        info = configure.get_app_info()
        self.local_instance = {
            'hostName': hostName,
            'app': info.get("name"),
            'ipAddr': localAddress,
            'port': {
                '$': info.get("port")
            }
        }

    @property
    def isLocal(self):
        return True

    @property
    def client():
        raise RuntimeError('LocalDiscoveryClient不支持client属性')

    def start(self):
        # 什么也不做
        pass

    def register(self):
        # 什么也不做
        pass

    def unregister(self):
        # 什么也不做
        pass

    def load_config(self):
        return configure
