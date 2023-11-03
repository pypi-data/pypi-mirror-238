from __future__ import absolute_import
from ..config import configure

configure.merge()
print(configure.get_app_info())
print(configure.get_config())
c = configure.get_config('eureka')

print(c)
