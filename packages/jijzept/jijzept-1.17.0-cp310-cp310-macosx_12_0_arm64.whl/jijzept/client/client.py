from __future__ import annotations

import base64

from typing import Any

import pydantic, rapidjson, requests, zstandard

from jijzept.config import Config
from jijzept.config.path_type import PATH_TYPE
from jijzept.utils import with_measuring_time


class JijZeptClient:
    config: Config
    query_url: pydantic.AnyUrl
    post_url: pydantic.AnyUrl
    token: str | dict
    proxy: pydantic.AnyUrl | None

    zstd_decompressor: zstandard.ZstdDecompressor
    zstd_compressor: zstandard.ZstdCompressor

    ZSTD_HEADERS: dict
    JSON_HEADERS: dict

    instance_id: str | None
    req_solution_id: str | None

    def __init__(
        self,
        *,
        url: str | None = None,
        token: str | None = None,
        proxy: str | None = None,
        config: PATH_TYPE | None = None,
        config_env: str = "default",
    ):
        """Constructor of JijZept client.

        Args:
            url (str | None, optional): url. Defaults to None.
            token (str | None, optional): token string. Defaults to None.
            proxy (str | None, optional): proxy string. Defaults to None.
            config (PATH_TYPE | None, optional): config path. Defaults to None.
            config_env (str, optional): config_env. Defaults to "default".
        """

        config = Config(
            url=url, token=token, proxy=proxy, config=config, config_env=config_env
        )
        object.__setattr__(self, "config", config)
        # url = self.config.url
        # self.url = url if url[-1] != '/' else url[:-1]
        query_url = config.query_url
        object.__setattr__(
            self, "query_url", query_url if query_url[-1] != "/" else query_url[:-1]
        )

        post_url = self.config.post_url
        object.__setattr__(
            self, "post_url", post_url if post_url[-1] != "/" else post_url[:-1]
        )

        object.__setattr__(self, "token", config.token)

        object.__setattr__(self, "proxy", config.proxy)

        zstd_decompressor: zstandard.ZstdDecompressor = zstandard.ZstdDecompressor()
        object.__setattr__(self, "zstd_decompressor", zstd_decompressor)

        zstd_compressor: zstandard.ZstdCompressor = zstandard.ZstdCompressor(
            level=zstandard.MAX_COMPRESSION_LEVEL,
            write_checksum=True,
            write_content_size=True,
            write_dict_id=True,
            threads=-1,
        )
        object.__setattr__(self, "zstd_compressor", zstd_compressor)

        zstd_headers = {
            "Content-Type": "application/zstd",
            "Ocp-Apim-Subscription-Key": config.token,
        }
        object.__setattr__(self, "ZSTD_HEADERS", zstd_headers)

        json_headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": config.token,
        }
        object.__setattr__(self, "JSON_HEADERS", json_headers)

        object.__setattr__(self, "instance_id", None)
        object.__setattr__(self, "req_solution_id", None)

        object.__setattr__(self, "__slots__", ())

    @with_measuring_time("post_problem_and_instance_data")
    def post_instance(
        self, instance_type: str, instance: dict[str, Any], endpoint: str = "/instance"
    ) -> str:
        """Send instance to JijZept.

        Args:
            instance_type (str): instance_type of the instance
            instance (Dict[str, Any]): serialized instance object. This object is compressed by zstandard
            endpoint (str, optional): endpoint. Defaults to "/instance".

        Raises:
            TypeError: `instance_type` or `instance`

        Returns:
            str: returned instance id
        """
        if not isinstance(instance_type, str):
            raise TypeError(f"'instance_type' is `str`, not `{type(instance_type)}`")
        if not isinstance(instance, dict):
            raise TypeError(f"instance is `dict`, not `{type(instance)}`")

        endpoint = endpoint[:-1] if endpoint[-1] == "/" else endpoint

        # ------- Upload instance data to JijZept ---------
        upload_endpoint = self.post_url + endpoint + "/upload"
        # encode instance
        json_data = rapidjson.dumps(
            instance,
            ensure_ascii=False,
            write_mode=rapidjson.WM_COMPACT,
        )
        json_binary = json_data.encode("utf-8")
        compressed_binary = self.zstd_compressor.compress(json_binary)
        res = requests.post(
            upload_endpoint,
            headers=self.ZSTD_HEADERS,
            proxies=self.proxy,
            data=compressed_binary,
            stream=True,
        )

        status_check(res)

        # res_body => {
        #   "file_name": str
        # }
        res_body: dict = res.json()
        self.instance_data_id = res_body["instance_data_id"]
        # -----------------------------------------------

        # ---- `instance_type` registration to JijZept-API -----
        regist_endpoint = self.post_url + endpoint
        dict_data = {
            "instance_type": instance_type,
            "instance_data_id": self.instance_data_id,
        }
        req_body = rapidjson.dumps(
            dict_data,
            ensure_ascii=False,
            write_mode=rapidjson.WM_COMPACT,
        )
        res = requests.post(
            regist_endpoint,
            headers=self.JSON_HEADERS,
            proxies=self.proxy,
            data=req_body,
        )
        status_check(res)

        self.instance_id = res.json()["instance_id"]
        # ------------------------------------------------------
        return self.instance_id

    @with_measuring_time("request_queue")
    def submit_solve_query(
        self,
        queue_name: str,
        solver_name: str,
        parameters: dict,
        instance_id: str | None = None,
        timeout: int | float | None = None,
        endpoint: str = "/query/solution",
    ) -> dict[str, str]:
        """Submit solve request to JijZept.

        Args:
            queue_name (str): queue_name
            solver_name (str): solver_name
            parameters (dict): parameters to be sent to queue
            instance_id (Optional[str], optional): problem instance id. Defaults to None.
            timeout (int | float | None , optional): timeout paraemter [second]. if None, timeout is set to inifite.
            Defaults to None.
            endpoint (str, optional): endpoint. Defaults to "/query/solution".

        Returns:
            Dict[str, str]: solution id information.
        """
        if self.instance_id is None and instance_id is None:
            message = "solve_request() missing 1 "
            message += "require positional argument: 'instance_id'"
            raise TypeError(message)

        if not isinstance(solver_name, str):
            raise TypeError(f"`solver_name` is str. not {type(solver_name)}")

        if not isinstance(parameters, dict):
            raise TypeError(f"`parameters` is dict. not {type(parameters)}")

        instance_id = self.instance_id if instance_id is None else instance_id

        query_endopoint = self.query_url + endpoint
        dict_data = {
            "instance_id": instance_id,
            "solver_params": parameters,
            "queue_name": queue_name,
            "solver": solver_name,
            "timeout": timeout,
        }
        json_data = rapidjson.dumps(
            dict_data,
            ensure_ascii=False,
            write_mode=rapidjson.WM_COMPACT,
        )
        res = requests.post(
            query_endopoint,
            headers=self.JSON_HEADERS,
            proxies=self.proxy,
            data=json_data,
        )
        status_check(res)

        # res_body => {
        #   "solution_id": str,
        # }
        res_body: dict = res.json()
        self.req_solution_id = res_body["solution_id"]

        return res_body

    @with_measuring_time("fetch_result")
    def fetch_result(
        self, solution_id: str | None = None, endpoint: str = "/query/solution"
    ) -> dict:
        """Fetch result and solution from JijZept.

        Args:
            solution_id (Optional[str], optional): solution id. Defaults to None.
            endpoint (str, optional): endpoint. Defaults to "/query/solution".

        Returns:
            dict: serialized result of derived information
        """
        if self.req_solution_id is None and solution_id is None:
            message = "fetch_result() missing 1 "
            message += "require positional argument: 'solution_id'"
            raise TypeError(message)

        solution_id = self.req_solution_id if solution_id is None else solution_id

        fetch_endpoint = self.query_url + endpoint

        params = {"solution_id": solution_id}

        res = requests.get(
            fetch_endpoint, headers=self.ZSTD_HEADERS, proxies=self.proxy, params=params
        )

        status_check(res)
        data = res.content
        # If the response is from AWS, decode the content with Base64.
        if res.headers.get("x-amzn-RequestPath") == "GET-solution":
            data = base64.b64decode(data)
        decompressed_data = self.zstd_decompressor.decompress(data)
        res_body = rapidjson.loads(decompressed_data)

        return res_body


def status_check(res: requests.Response) -> None:
    """Do status check of response data.
    If request has some HTTPError, this function raises Exception.

    Args:
        res (requests.Response): response from http request

    Raises:
        requests.exceptions.HTTPError: if response has some error.
    """

    http_error_msg: str = ""
    if isinstance(res.reason, bytes):
        try:
            reason = res.reason.decode("utf-8")
        except UnicodeDecodeError:
            reason = res.reason.decode("iso-8859-1")
    else:
        reason = res.reason

    if 400 <= res.status_code < 500:
        http_error_msg = f"{res.status_code} Client Error: {reason} for url {res.url}"
    elif 500 <= res.status_code < 600:
        http_error_msg = f"{res.status_code} Server Error: {reason} for url {res.url}"

    if http_error_msg:
        try:
            res_body = rapidjson.loads(res.text)
        except rapidjson.JSONDecodeError:
            res_body = res.text

        raise requests.exceptions.HTTPError(
            http_error_msg,
            res_body, 
            response=res
        )
