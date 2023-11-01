from __future__ import annotations

import dataclasses
import time
import typing as typ

import jijmodeling as jm

from google.protobuf.text_encoding import CEscape

from jijzept.client import JijZeptClient
from jijzept.config.path_type import PATH_TYPE
from jijzept.entity.schema import SolverType
from jijzept.exception.exception import (
    JijZeptClientValidationError,
    JijZeptSolvingFailedError,
    JijZeptSolvingUnknownError,
    JijZeptSolvingValidationError,
)
from jijzept.instance_translator.instance_translator import InstanceTranslator
from jijzept.post_api import post_instance, post_query
from jijzept.response import JijModelingResponse
from jijzept.response.base import APIStatus
from jijzept.type_annotation import FixedVariables, InstanceData
from jijzept.utils import serialize_fixed_var


# This class provides only a constructor,
# so each sampler should implement its own methods such as .sample_model.
# In addition, each sampler specifies the API to be connected by specifying "jijmodeling_solver_type",
# so be sure to implement it.
class JijZeptBaseSampler:
    """Parent class for each sampler in JijZept.

    This class only provide the constructor.
    The actual sampling method are implemented by each sampler.
    """

    jijmodeling_solver_type: SolverType

    def __init__(
        self,
        token: str | None = None,
        url: str | None = None,
        proxy: str | None = None,
        config: PATH_TYPE | None = None,
        config_env: str = "default",
    ):
        """Sets token and url.

        If you do not set any arguments, JijZept configuration file is used.
        If you set the url or token here, that will be used as the priority setting for connecting to the API.
        See JijZeptClient for details.

        Args:
            token (str | None, optional): Token string. Defaults to None.
            url (str | None, optional): API URL. Defaults to None.
            proxy (str | None, optional): Proxy URL. Defaults to None.
            config (str | None, optional): Config file path. Defaults to None.
            config_env (str, optional): configure environment name. Defaults to 'default'.

        Raises:
            TypeError: `token`, `url`, or `config` is not str.
        """
        self.client = JijZeptClient(
            url=url, token=token, proxy=proxy, config=config, config_env=config_env
        )

    def upload_instance(
        self,
        problem: jm.Problem,
        feed_dict: InstanceData,
        system_time: jm.SystemTime = jm.SystemTime(),
    ) -> str:
        """Upload instance.

        An instance is a pair of `problem` and `feed_dict`.
        This method stores the instance into the cloud.

        Args:
            problem (jm.Problem): Mathematical expression of JijModeling.
            feed_dict (dict[str, int | float | numpy.integer | numpy.floating | numpy.ndarray | list]): The actual values to be assigned to the placeholders.
            system_time (jm.SystemTime):  Object to store upload time.

        Returns:
            str: The ID of the uploaded instance.

        Examples:
            ```python
            import jijzept as jz
            import jijmodeling as jm

            n = jm.Placeholder('n')
            x = jm.BinaryVar('x', shape=(n,))
            d = jm.Placeholder('d', ndim=1)
            i = jm.Element("i", belong_to=(n,))
            problem = jm.Problem('problem')
            problem += jm.Sum(i, d[i] * x[i])

            # initialize sampler
            sampler = jz.JijSASampler(config='config.toml')

            # upload instance
            instance_id = sampler.upload_instance(problem, {'n': 5, 'd': [1,2,3,4,5]})

            # sample uploaded instance
            sample_set = sampler.sample_instance(instance_id)
            ```
        """
        return upload_instance(
            client=self.client,
            problem=problem,
            instance_data=feed_dict,
            system_time=system_time,
        )


@dataclasses.dataclass
class ParameterSearchParameters:
    """Data class for parameter_search_parameters."""

    multipliers: dict[str, float] = dataclasses.field(default_factory=lambda: {})
    mul_search: bool = False
    num_search: int = 15
    algorithm: str | None = None
    normalize_qubo: bool = True


def sample_model(
    client: JijZeptClient,
    solver: str,
    queue_name: str,
    problem: jm.Problem,
    instance_data: InstanceData,
    fixed_variables: FixedVariables,
    parameter_search_parameters: ParameterSearchParameters,
    max_wait_time: int | float | None,
    sync: bool,
    **kwargs,
) -> JijModelingResponse:
    """
    Solver using the given parameters, returns a JijModelingResponse object.

    Args:
        client (JijZeptClient): JijZept client object.
        solver (str): Solver type.
        queue_name (str): Queue name to use.
        problem (jm.Problem): The problem to be solved.
        instance_data (dict[str, int | float | numpy.integer | numpy.floating | numpy.ndarray | list]): Instance data.
        fixed_variables (dict[str, dict[tuple[int, ...], int]]): Fixed variables.
        parameter_search_parameters (ParameterSearchParameters): Parameters for parameter search.
        max_wait_time (int | float | None): Maximum time to wait for the response, in seconds.
        sync (bool): Whether to wait for the response.

    Returns:
        JijModelingResponse: Stores minimum energy samples and statistics of the computation.

    Raises:
        JijZeptSolvingFailedError: If the computation failed to solve the problem.
        JijZeptSolvingUnknownError: If the computation ended in an unknown error.
        JijZeptSolvingValidationError: If the computation failed to validate the input parameters.
    """
    start = time.time()
    system_time = jm.SystemTime()

    instance_id = upload_instance(
        client=client,
        problem=problem,
        instance_data=instance_data,
        system_time=system_time,
    )

    response = sample_instance(
        client=client,
        solver=solver,
        queue_name=queue_name,
        instance_id=instance_id,
        fixed_variables=fixed_variables,
        parameter_search_parameters=parameter_search_parameters,
        max_wait_time=max_wait_time,
        sync=sync,
        system_time=system_time,
        **kwargs,
    )

    response.sample_set.measuring_time = jm.MeasuringTime(
        solve=response.sample_set.measuring_time.solve,
        system=response.sample_set.measuring_time.system,
        total=time.time() - start,
    )

    return response


def upload_instance(
    client: JijZeptClient,
    problem: jm.Problem,
    instance_data: InstanceData,
    system_time: jm.SystemTime = jm.SystemTime(),
) -> str:
    """
    This function makes `problem` and `instance_data` into sendable instance, then store it into the cloud.

    Args:
        client (JijZeptClient): JijZept client object.
        problem (jm.Problem): Mathematical expression of JijModeling.
        instance_data (dict[str, int | float | numpy.integer | numpy.floating | numpy.ndarray | list]): The actual values to be assigned to the placeholders.
        system_time (jm.SystemTime):  Object to store upload time.

    Returns:
        str: The ID of the uploaded instance.
    """

    instance = {
        "mathematical_model": CEscape(jm.to_protobuf(problem), as_utf8=False),
        "instance_data": InstanceTranslator.instance_translate(instance_data),
    }

    instance_id = post_instance(
        client=client,
        instance_type="JijModeling",
        instance=instance,
        system_time=system_time,
    )

    return instance_id


def sample_instance(
    client: JijZeptClient,
    solver: str,
    queue_name: str,
    instance_id: str,
    fixed_variables: FixedVariables,
    parameter_search_parameters: ParameterSearchParameters,
    max_wait_time: int | float | None,
    sync: bool,
    system_time: jm.SystemTime = jm.SystemTime(),
    **kwargs,
) -> JijModelingResponse:
    """
    Solver using the given parameters, returns a JijModelingResponse object.

    Args:
        client (JijZeptClient): JijZept client object.
        solver (str): Solver type.
        queue_name (str): Queue name to use.
        instance_id (str): The ID of the uploaded instance.
        fixed_variables (dict[str, dict[tuple[int, ...], int]]): Fixed variables.
        parameter_search_parameters (ParameterSearchParameters): Parameters for parameter search.
        max_wait_time (int | float | None): Maximum time to wait for the response, in seconds.
        sync (bool): Whether to wait for the response.
        system_time (jm.SystemTime): Object to store system times other than upload time.

    Returns:
        JijModelingResponse: Stores minimum energy samples and statistics of the computation.

    Raises:
        JijZeptSolvingFailedError: If the computation failed to solve the problem.
        JijZeptSolvingUnknownError: If the computation ended in an unknown error.
        JijZeptSolvingValidationError: If the computation failed to validate the input parameters.
    """

    param_dict = dataclasses.asdict(parameter_search_parameters)
    param_dict["fixed_variables"] = serialize_fixed_var(fixed_variables)
    param_dict.update(kwargs)

    response = post_query(
        JijModelingResponse,
        client=client,
        instance_id=instance_id,
        queue_name=queue_name,
        solver=solver,
        parameters=param_dict,
        timeout=max_wait_time,
        sync=sync,
        system_time=system_time,
    )

    # Raise error if the problem is not solved.
    if response.status == APIStatus.FAILED:
        raise JijZeptSolvingFailedError(
            response.error_message.get("message", "The problem is not solved.")
        )
    elif response.status == APIStatus.UNKNOWNERROR:
        raise JijZeptSolvingUnknownError(
            response.error_message.get("message", "The problem is not solved.")
        )
    elif response.status == APIStatus.VALIDATIONERROR:
        raise JijZeptSolvingValidationError(
            response.error_message.get("message", "The problem is not solved.")
        )

    return response


def merge_params_and_kwargs(
    parameters: dataclasses._DataclassT | None,
    kwargs: dict[str, typ.Any],
    param_cls: typ.Type[dataclasses._DataclassT],
) -> dict[str, typ.Any]:
    """
    Merge the set of parameters defined by `parameters` and the set of parameters
    defined by `kwargs`, giving precedence to the values defined in `kwargs`.

    Args:
        parameters: A instance of the dataclass defining the set of parameters.
        kwargs: A dictionary containing the values of the parameters to be used in a computation.
        param_cls: the dataclass to be used for `parameters`.

    Returns:
        A dictionary containing the merged set of parameters and keyword arguments.
    """
    from jijzept.sampler import thirdparty

    param_dict: dict[str, typ.Any] = {}
    if parameters is None:
        _parameters = dataclasses.asdict(param_cls())
    else:
        _parameters = dataclasses.asdict(parameters)

    if param_cls.__name__ in thirdparty.__all__:
        param_dict.update({"parameters": _parameters})
    else:
        param_dict.update(_parameters)

    for key, value in kwargs.items():
        param_dict[key] = value
    return param_dict


def check_kwargs_against_dataclass(
    kwargs: dict[str, typ.Any],
    param_cls: typ.Type,
) -> None:
    """
    Check if the keyword arguments have a key other than the field names of specified dataclass.

    Args:
        kwargs: A dictionary of keyword arguments to be checked.
        param_cls: A type representing the class to be used for `parameters`.

    Raises:
        JijZeptClientValidationError: If **kwargs contain extra keyword argument.
    """
    field_names = dataclasses.asdict(param_cls()).keys()
    extra_kwargs: list[str] = []

    for key in kwargs.keys():
        if key not in field_names:
            extra_kwargs.append(f"`{key}`")

    if len(extra_kwargs) > 0:
        raise JijZeptClientValidationError(
            f"Extra keyword argument is permmited: {','.join(extra_kwargs)}. "
            f"**kwargs are allowed only for field names of {param_cls.__name__}."
        )
