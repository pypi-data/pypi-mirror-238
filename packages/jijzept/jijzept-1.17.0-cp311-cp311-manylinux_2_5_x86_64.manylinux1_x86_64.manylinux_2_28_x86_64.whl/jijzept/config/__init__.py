from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

import jijzept.config.handle_config as handle_config
import jijzept.config.path_type as path_type

from jijzept.config.handle_config import Config

__all__ = [
    "handle_config",
    "path_type",
    "Config",
]
