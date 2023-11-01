from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

import jijzept.setting.setting as setting

from jijzept.setting.setting import load_config

__all__ = ["setting", "load_config"]
