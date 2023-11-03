from typing import Dict, List
import json


class WebError(RuntimeError):
    def __init__(self,
                 message: str,
                 code: str = None,
                 desc: str = None,
                 headers: Dict[str, str] = {},
                 status: int = 400):
        super().__init__(message)
        self.code = code
        self.desc = desc
        self.headers = headers
        self.status = status
        self.details: List[str] = []

    def __dir__(self):
        # 返回自定义的属性和方法列表
        return super.__dir__() + \
            ['code', 'desc', 'headers', 'status', 'details']

    def __str__(self):
        obj = dict(self.__dict__)
        obj['message'] = super().__str__()
        return json.dumps(obj, ensure_ascii=False)
