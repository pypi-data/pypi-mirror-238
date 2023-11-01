from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

import jijzept.post_api.post_api as post_api

from jijzept.post_api.post_api import (
    JijZeptAPIError,
    _fetch_result,
    _from_json_obj,
    post_instance,
    post_instance_and_query,
    post_query,
)

__all__ = [
    "post_api",
    "JijZeptAPIError",
    "_fetch_result",
    "_from_json_obj",
    "post_instance",
    "post_query",
    "post_instance_and_query",
]
