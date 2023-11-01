from __future__ import annotations

import logging, os, sys, time

from logging import getLogger
from typing import Any, Dict, Type, TypeVar

import jijmodeling as jm

from jijzept.client import JijZeptClient
from jijzept.response import APIStatus, BaseResponse, JijModelingResponse
from jijzept.utils import with_measuring_time

ResponseType = TypeVar("ResponseType", bound=BaseResponse)

logger = getLogger(__name__)

if os.environ.get("JIJZEPT_VERBOSE") is None:
    pass
else:
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

# set the default timeout to 1 min if not specified.
DEFAULT_TIMEOUT_SEC = 60


class JijZeptAPIError(Exception):
    pass


def post_instance_and_query(
    ResponseType: Type[TypeVar("ResponseType", bound="BaseResponse")],
    client: JijZeptClient,
    instance_type: str,
    instance: Dict[str, Any],
    queue_name: str,
    solver: str,
    parameters: dict,
    timeout: int | float | None = None,
    sync: bool = True,
):
    """Low-level API for sending instance and solve request to JijZept.

    Args:
        client (JijZeptClient): JijZept client object
        instance_type (str): instance type
        instance (Dict[str, Any]): serialized instance object.
        queue_name (str): queue_name that specifies which solver the request to be sent to.
        solver (str): solver string that is used in JijZept solvers.
        parameters (dict): additional parameters to be sent to JijZept solvers.
        timeout (int | float | None, optional): solver timeout [second]
        ResponseType (Type[TypeVar, optional): Response Type. Defaults to "BaseResponse")].
        sync (bool, optional): set sync model. if True, this function does polling until the solution status is
        changed from `PENDING` or `RUNNING`. Defaults to True.

    Returns:
        ResponseType: response object
    """
    system_time = jm.SystemTime()

    instance_id = post_instance(
        client=client,
        instance_type=instance_type,
        instance=instance,
        system_time=system_time,
    )

    return post_query(
        ResponseType=ResponseType,
        client=client,
        instance_id=instance_id,
        queue_name=queue_name,
        solver=solver,
        parameters=parameters,
        timeout=timeout,
        sync=sync,
        system_time=system_time,
    )


def post_instance(
    client: JijZeptClient,
    instance_type: str,
    instance: Dict[str, Any],
    system_time: jm.SystemTime = jm.SystemTime(),
) -> str:
    """Low-level API for sending instance to JijZept.

    Args:
        client (JijZeptClient): JijZept client object
        instance_type (str): instance type
        instance (Dict[str, Any]): serialized instance object.
        system_time (jm.SystemTime): Object to store upload time.

    Returns:
        str: The ID of the uploaded instance.
    """
    logger.info("uploading instance ...")
    instance_id = client.post_instance(instance_type, instance, system_time=system_time)
    logger.info(f"upload success instance_id={instance_id}.")

    return instance_id


def post_query(
    ResponseType: Type[TypeVar("ResponseType", bound="BaseResponse")],
    client: JijZeptClient,
    instance_id: str,
    queue_name: str,
    solver: str,
    parameters: dict,
    timeout: int | float | None = None,
    sync: bool = True,
    system_time: jm.SystemTime = jm.SystemTime(),
):
    """Low-level API for sending solve request to JijZept.

    Args:
        client (JijZeptClient): JijZept client object
        instance_id (str): The ID of the uploaded instance.
        queue_name (str): queue_name that specifies which solver the request to be sent to.
        solver (str): solver string that is used in JijZept solvers.
        parameters (dict): additional parameters to be sent to JijZept solvers.
        timeout (int | float | None, optional): solver timeout [second]
        ResponseType (Type[TypeVar, optional): Response Type. Defaults to "BaseResponse")].
        sync (bool, optional): set sync model. if True, this function does polling until the solution status is changed from `PENDING` or `RUNNING`. Defaults to True.
        system_time (jm.SystemTime): Object to store system times other than upload time.

    Returns:
        ResponseType: response object
    """
    logger.info("submitting query ...")
    actual_timeout = DEFAULT_TIMEOUT_SEC if timeout is None else timeout
    solver_res = client.submit_solve_query(
        queue_name,
        solver,
        parameters,
        instance_id,
        actual_timeout,
        system_time=system_time,
    )
    logger.info(f"submitted to the queue.")
    logger.info(f'Your solution_id is {solver_res["solution_id"]}.')

    if sync:
        response = _fetch_result(
            ResponseType, client, solver_res, system_time=system_time
        )
        if isinstance(response, ResponseType):
            return response
        else:
            res_obj = _from_json_obj(ResponseType, response, system_time=system_time)
            if isinstance(res_obj, JijModelingResponse):
                res_obj.sample_set.measuring_time = jm.MeasuringTime(
                    solve=(
                        jm.SolvingTime()
                        if res_obj.sample_set.measuring_time.solve is None
                        else res_obj.sample_set.measuring_time.solve
                    ),
                    system=system_time,
                    total=res_obj.sample_set.measuring_time.total,
                )
            return res_obj
    else:
        return ResponseType.empty_response(
            APIStatus.PENDING, client, solver_res["solution_id"]
        )


@with_measuring_time("fetch_result")
def _fetch_result(ResponseType, client, solver_res):
    """Polls the API for the result of a solver's solution and returns the response as a `ResponseType` object.

    Args:
        ResponseType: A type that can be instantiated to create a response object.
        client: An instance of the client used to access the API.
        solver_res: A dictionary containing the solver's solution ID.

    Returns:
        A `ResponseType` object representing the response from the API.

    Raises:
        RuntimeError: If an unpredicted status is returned by the API.

    """
    status = "PENDING"
    show_running_flag = False

    polling_count = 0
    while (status == APIStatus.PENDING.value) or (status == APIStatus.RUNNING.value):
        response = client.fetch_result(solver_res["solution_id"])
        status = response["status"]
        if status == APIStatus.PENDING.value:
            if not show_running_flag:
                logger.info("pending...")
                show_running_flag = True
        elif status == APIStatus.RUNNING.value:
            if not show_running_flag:
                logger.info("running...")
                show_running_flag = True
        elif status == APIStatus.SUCCESS.value:
            return response
        elif status == APIStatus.FAILED.value:
            return ResponseType.empty_response(
                APIStatus.FAILED,
                client,
                solver_res["solution_id"],
                err_dict=response["solution"],
            )
        elif status == APIStatus.VALIDATIONERROR.value:
            return ResponseType.empty_response(
                APIStatus.VALIDATIONERROR,
                client,
                solver_res["solution_id"],
                err_dict=response["solution"],
            )
        elif status == APIStatus.UNKNOWNERROR.value:
            return ResponseType.empty_response(
                APIStatus.UNKNOWNERROR,
                client,
                solver_res["solution_id"],
                err_dict=response["solution"],
            )
        else:
            raise RuntimeError(f"Unpredicted status {status}.")
        time.sleep(2)
        polling_count = polling_count + 1
        if polling_count == 10:
            # show hints if polling is repeated certain times
            logger.info(f"It takes a lot of time to get the solution...")


@with_measuring_time("deserialize_solution")
def _from_json_obj(ResponseType, response):
    """Deserializes a JSON response from the API into a `ResponseType` object and sets its status to `APIStatus.SUCCESS`.

    Args:
        ResponseType: A type that can be instantiated to create a response object.
        response: A dictionary containing the JSON response from the API.

    Returns:
        A `ResponseType` object representing the deserialized response from the API.

    Raises:
        ValueError: If the response cannot be converted to `ResponseType`.
    """
    try:
        solution = response["solution"]
        res_obj = ResponseType.from_json_obj(solution)
    except TypeError as exc:
        raise ValueError(
            f"{solution} cannot be converted to {type(ResponseType)}."
        ) from exc
    else:
        res_obj.set_status(APIStatus.SUCCESS)
        return res_obj
