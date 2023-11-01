from __future__ import annotations

import dataclasses
import os
import pathlib
import typing as typ

from urllib.parse import ParseResult, urlparse

import pydantic, toml

from jijzept.config.path_type import PATH_TYPE
from jijzept.exception.exception import ConfigError

# DEFAULT SETTING
CONFIG_PATH: pydantic.DirectoryPath = pathlib.Path(
    pathlib.Path.home(), pathlib.Path(".jijzept")
)
DEFAULT_CONFIG_FILE: pydantic.FilePath = pathlib.Path("config.toml")


def config_file_path(
    file_path: typ.Union[pathlib.Path, str, None]
) -> typ.Optional[pathlib.Path]:
    """Get config file path.

    Configuration files are explored in the following order
    When found, the path to the file is returned, or None if not found.
    If the user specifies a file path in `file_path` arguments, it is returned in preference to all of the following.

    The search goes for the `jijzept` and `jijzept_config.toml` files in the following directories.

    1. Current directory: pathlib.Path().cwd()
    2. $XDG_CONFIG_HOME
    3. ~/.config

    The search order of this function is the priority order of config files in JijZept.

    Args:
        file_path (typ.Union[pathlib.Path, str, None]): file path. Defaults to None.

    Returns:
        pathlib.Path | None: config file path
    """
    if isinstance(file_path, str):
        return pathlib.Path(file_path)
    elif isinstance(file_path, pathlib.Path):
        return pathlib.Path(file_path)
    elif isinstance(file_path, os.PathLike):
        return pathlib.Path(file_path)
    elif isinstance(file_path, pathlib.PurePath):
        return pathlib.Path(file_path)
    elif file_path is not None:
        raise TypeError(f"'{file_path}' type is '{type(file_path)}' not path.")

    DOT_DIR_CONFIG: pydantic.FilePath = pathlib.Path(
        pathlib.Path(".jijzept"), pathlib.Path("config.toml")
    )
    JIJZEPT_CONFIG_TOML: pydantic.FilePath = pathlib.Path("jijzept_config.toml")

    config_file_names = [DOT_DIR_CONFIG, JIJZEPT_CONFIG_TOML]
    # 1. check current directory
    current_dir: pydantic.DirectoryPath = pathlib.Path().cwd()
    for config_file in config_file_names:
        config_path = pathlib.Path(current_dir, config_file)
        if config_path.exists():
            return config_path

    # 2. check $XDG_CONFIG_HOME
    XDG_CONFIG_HOME = "XDG_CONFIG_HOME"
    if XDG_CONFIG_HOME in os.environ:
        xdg_config_home_path: pydantic.DirectoryPath = pathlib.Path(
            os.environ[XDG_CONFIG_HOME]
        )
        for config_file in config_file_names:
            config_path = pathlib.Path(xdg_config_home_path, config_file)
            if config_path.exists():
                return config_path

    # 3. check ~/.config/
    CONFIG_HOME: pydantic.DirectoryPath = pathlib.Path(
        pathlib.Path.home(), pathlib.Path(".config")
    )
    for config_file in config_file_names:
        config_path = pathlib.Path(CONFIG_HOME, config_file)
        if config_path.exists():
            return config_path

    return None


def create_config(
    *,
    token: str,
    host_url: pydantic.HttpUrl,
    config_path: pydantic.FilePath = CONFIG_PATH,
) -> pydantic.FilePath:
    """Create new config file with the given `token` and `host_url` values.

    Args:
        token (str): The token to set in the config file.
        host_url (pydantic.HttpUrl): The host URL to set in the config file.
        config_path (pydantic.FilePath, optional): The path to the directory where the config file should be created. Defaults to CONFIG_PATH.

    Raises:
        FileExistsError: If the config file already exists.

    Returns:
        pydantic.FilePath: The path to the newly created config file.
    """
    if isinstance(config_path, str):
        config_path = pathlib.Path(config_path)
    elif isinstance(config_path, pathlib.Path):
        config_path = pathlib.Path(config_path)
    elif isinstance(config_path, os.PathLike):
        config_path = pathlib.Path(config_path)
    elif isinstance(config_path, pathlib.PurePath):
        config_path = pathlib.Path(config_path)
    elif config_path is not None:
        raise TypeError(f"'{config_path}' type is '{type(config_path)}' not path.")

    if config_path.is_file():
        raise FileExistsError
    elif config_path.is_dir():
        pass
    else:
        pathlib.Path(config_path).mkdir(parents=True, exist_ok=True)

    config_dict: dict = {"default": {"url": host_url, "token": token}}
    # save config file's
    config_file_path: pydantic.FilePath = pathlib.Path(config_path, DEFAULT_CONFIG_FILE)
    if config_file_path.is_file():
        raise FileExistsError
    with config_file_path.open(mode="w") as f:
        toml.dump(config_dict, f)

    return config_file_path


def load_config(*, file_path: pathlib.Path, config: str = "default") -> dict:
    """Load config file (TOML file).

    Args:
        file_path (pathlib.Path): path to config file.
        config (str): loading enviroment name. Defaults to 'default'.

    Raises:
        TypeError: if 'config' enviroment is not defined in config file.

    Returns:
        dict: ex. {'token': 'xxxx', 'url': 'xxxx'}
    """
    if not file_path.is_file():
        raise FileNotFoundError(file_path)
    with file_path.open(mode="r") as f:
        toml_setting_file = toml.load(f)
    if config not in toml_setting_file:
        raise ConfigError(f"'{config}' is not define in config file ({file_path}).")
    return toml_setting_file[config]


def _query_and_post_url(*, url: pydantic.HttpUrl) -> dict[str, str]:
    """Given a URL, returns a dictionary with its `query_url` and `post_url`.

    Args:
        url (pydantic.HttpUrl): The URL.

    Returns:
        dict: A dictionary containing the `query_url` and `post_url`.
    """
    parsed = urlparse(str(url))
    if not parsed.path:
        path = parsed.path + "/query"
    elif parsed.path[-1] != "/":
        path = parsed.path + "/query"
    else:
        path = parsed.path + "query"
    parsed_post_url = ParseResult(
        parsed.scheme,
        parsed.netloc,
        path,
        parsed.params,
        parsed.query,
        parsed.fragment,
    ).geturl()
    return {"query_url": str(url), "post_url": parsed_post_url}


@dataclasses.dataclass
class UrlInfo:
    """Class that holds the `query_url` and `post_url` of an API endpoint."""

    query_url: pydantic.HttpUrl
    post_url: pydantic.HttpUrl


def _get_url_info(
    *, url: str | dict[str, str] | None = None, config_data: dict[str, str]
) -> UrlInfo:
    """Retrieve URL information for JijZept API.

    Args:
        url (str | dict[str, str] | None, optional): Endpoint for connecting to JijZept API. If you want to set
            `query_url` and `post_url` separately, use a `dict` with each as a key. Defaults to None.
        config_data (dict[str, str]): The contents of the configuration file.

    Raises:
        KeyError: Raised if the `url` argument is a dictionary and does not contain both `post_url` and `query_url`.
        TypeError: Raised if the `url` argument is not a string or a dictionary.
        pydantic.error_wrappers.ValidationError: Raised if the URL schema is incorrect.

    Returns:
        UrlInfo: An object containing the query and post URLs.
    """
    adapter = pydantic.TypeAdapter(pydantic.HttpUrl)
    # check url schema is correct or not.
    _query_post_url: dict[str, str]
    if isinstance(url, dict):
        if "post_url" not in url or "query_url" not in url:
            raise KeyError("In `url`, please set `post_url` and `query_url`.")
        _query_post_url = url
    elif isinstance(url, str):
        correct_url = adapter.validate_python(url)
        _query_post_url = _query_and_post_url(url=correct_url)
    elif url is None:
        # `url` information should be set in config file.
        # parse url information from config file
        if "url" in config_data:
            correct_url = adapter.validate_python(config_data["url"])
            _query_post_url = _query_and_post_url(url=correct_url)
        elif "post_url" in config_data and "query_url" in config_data:
            _query_post_url = config_data
        else:
            raise ConfigError("`url` should be set in the arugment or config file.")
    else:
        raise TypeError(f"'{url}' type is '{type(url)}' not str or dict.")

    post_url: pydantic.HttpUrl = adapter.validate_python(_query_post_url["post_url"])
    query_url: pydantic.HttpUrl = adapter.validate_python(_query_post_url["query_url"])

    return UrlInfo(query_url=query_url, post_url=post_url)


def _get_token(*, token: str | None, config_data: dict[str, str]) -> str:
    if token is not None:
        return token

    if "token" not in config_data:
        raise ConfigError("`token` is needed in the arguments or config file.")

    return config_data["token"]


@dataclasses.dataclass
class Config:
    config_path: pathlib.Path
    url_info: UrlInfo
    token: str
    proxy: typ.Optional[pydantic.AnyUrl]
    additional_setting: typ.Dict[str, str]

    """
    JijZept API Config.

    Attributes:
        query_url (str): Endpoint for Query API.
        post_url (str): Endpoint for Post Instance API.
        proxy (str, optional): Proxy URL. Defaults to None.
        token (str): Secret token to connect API.
        additional_setting (dict[str, str]): Parameters for thirdparty samplers.

    Note:
        ### How to write config.toml
        Write `url` and `token` under [default], and ThirdpartySampler's parameters under [default.thirdparty-setting].
        The following is a config.toml example with ThirdpartySampler's parameters.
        ```
        [default]
        url = "https://api.jijzept.com/"
        token = "715df11165044899867df0f7bb8a60e9"

        [default.thirdparty-setting]
        da4_token = "da4df11165044899867df0f7bb8a60e9"
        da4_url = "https://jijcloud.da4.net/"
        ```
    """

    def __init__(
        self,
        *,
        url: typ.Union[str, dict[str, str], None] = None,
        token: typ.Optional[str] = None,
        proxy: typ.Optional[str] = None,
        config: typ.Optional[PATH_TYPE] = None,
        config_env: str = "default",
    ):
        """
        Args:
            url (str | dict[str, str] | None, optional): Endpoint for connecting to JijZept API. If you want to set
            `query_url` and `post_url` separately, use a `dict` with each as a key. Defaults to None.
            token (str | None, optional): token to connect JijZept API. Defaults to None.
            proxy (str | None, optional): proxy server. Defaults to None.
            config (PATH_TYPE | None, optional): config file path. Defaults to None.
            config_env (str, optional): config environment name. Defaults to "default".

        Raises:
            jijzept.exception.ConfigError: parse error.
            TypeError: url schema or config path is invaild.
            pydantic.error_wrappers.ValidationError: url schema or config path is invaild.
        """

        # Order of precedence
        # url, token, proxy > config, config_env
        # User can override a config by each arguments (ex. url, token).
        config_path = config_file_path(config)

        # Load config file
        config_data = {}
        if config_path is not None:
            config_data = load_config(file_path=config_path, config=config_env)

        # url info setting
        self.url_info = _get_url_info(url=url, config_data=config_data)
        # token setting
        self.token = _get_token(token=token, config_data=config_data)

        adapter = pydantic.TypeAdapter(pydantic.AnyUrl)

        # `proxy` setting
        if proxy is not None:
            self.proxy = str(adapter.validate_python(proxy))
        else:
            if "proxy" in config_data:
                self.proxy = str(adapter.validate_python(config_data["proxy"]))
            else:
                self.proxy = None

        self.additional_setting = {}
        # additional setting
        if "thirdparty-setting" in config_data:
            for key, value in config_data["thirdparty-setting"].items():
                if key[-4:] == "_url":  # case: url
                    self.additional_setting[key] = str(
                        adapter.validate_python(value)
                    )
                else:
                    self.additional_setting[key] = str(value)

        object.__setattr__(self, "__slots__", ())

    @property
    def query_url(self) -> str:
        return str(self.url_info.query_url)

    @property
    def post_url(self) -> str:
        return str(self.url_info.post_url)
