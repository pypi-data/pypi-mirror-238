from __future__ import absolute_import

from .abstarct_rule import AbstractRule


class SimpleRule(AbstractRule):
    def check_alive(self):
        apps = self._eureka.applications.get_application(self._app_id_upper)
        return len(apps.up_instances) > 0

    def _choose(self):
        if not self.check_alive():
            return None

        apps = self._eureka.applications.get_application(self._app_id_upper)
        inst = apps.up_instances[0]
        return inst
