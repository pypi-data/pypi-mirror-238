from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

import jijzept.exception.exception as exception

from jijzept.exception.exception import ConfigError, JijZeptClientError

__all__ = ["exception", "JijZeptClientError", "ConfigError"]
