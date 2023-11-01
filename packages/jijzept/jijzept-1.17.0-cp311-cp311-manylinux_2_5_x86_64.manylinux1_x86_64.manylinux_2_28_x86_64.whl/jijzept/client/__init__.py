from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

import jijzept.client.client as client

from jijzept.client.client import JijZeptClient, status_check

__all__ = ["client", "JijZeptClient", "status_check"]
