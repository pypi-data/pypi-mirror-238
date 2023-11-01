from __future__ import annotations

import typing as typ

from dataclasses import dataclass

import jijmodeling as jm

from jijzept.client import JijZeptClient
from jijzept.entity.schema import SolverType
from jijzept.exception import ConfigError
from jijzept.response import JijModelingResponse
from jijzept.sampler.base_sampler import (
    JijZeptBaseSampler,
    ParameterSearchParameters,
    check_kwargs_against_dataclass,
    merge_params_and_kwargs,
    sample_instance,
    sample_model,
)
from jijzept.type_annotation import FixedVariables, InstanceData

T = typ.TypeVar("T")


@dataclass
class JijLeapHybridCQMParameters:
    """Manage Parameters for using Leap Hybrid CQM Sampler.

    Attributes:
        time_limit (Optional[Union[int, float]]): the maximum run time, in seconds, the solver is allowed to work on the given problem. Must be at least the minimum required for the problem, which is calculated and set by default. It is deprecated to set this up due to high credit consumption.
        label (str): The problem label given to the dimod.SampelSet instance returned by the JijLeapHybridCQMSampler. Defaults to None.
    """

    time_limit: int | float | None = None
    label: str | None = None


class JijLeapHybridCQMSampler(JijZeptBaseSampler):
    """Sampler using Leap Hybrid CQM Sampler, which is D-Wave's Constrained Quandratic Model (CQM)."""

    jijmodeling_solver_type = SolverType(
        queue_name="thirdpartysolver", solver="DwaveLeap"
    )

    def __init__(
        self,
        token: str | None = None,
        url: str | None = None,
        proxy: str | None = None,
        config: str | None = None,
        config_env: str = "default",
        leap_token: str | None = None,
        leap_url: str | None = None,
    ) -> None:
        """Sets token and url.

        If `leap_token` and 'leap_url` are not specified in the arguments,
        JijZept configuration file is used.
        If `leap_token` and `leap_url` are specified in the arguments,
        that will be used as priority setting.

        Args:
            token (Optional[str]): Token string for JijZept.
            url (Optional[str]): API URL for JijZept.
            proxy (Optional[str]): Proxy URL. Defaults to None.
            config (Optional[str]): Config file path for JijZept.
            leap_token (Optional[str]): Token string for Dwave Leap.
            leap_url (Optional[str]): API URL for Dwave Leap.

        raises:
            ConfigError: if `leap_token` is not defined in the argument or config.toml.
        """
        self.client = JijZeptClient(
            url=url, token=token, proxy=proxy, config=config, config_env=config_env
        )

        if leap_token is None:
            if "leap_token" in self.client.config.additional_setting:
                self.leap_token = self.client.config.additional_setting["leap_token"]
            else:
                raise ConfigError(
                    "`leap_token` should be set in the argument or config file."
                )
        else:
            self.leap_token = leap_token

        if leap_url is None:
            if "leap_url" in self.client.config.additional_setting:
                self.leap_url = self.client.config.additional_setting["leap_url"]
            else:
                self.leap_url = None
        else:
            self.leap_url = leap_url

    def sample_model(
        self,
        model: jm.Problem,
        feed_dict: InstanceData,
        fixed_variables: FixedVariables | None = None,
        relax_list: typ.List[str] | None = None,
        parameters: JijLeapHybridCQMParameters | None = None,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str | None = None,
        **kwargs,
    ) -> JijModelingResponse:
        """Converts the given problem to dimod.ConstrainedQuadraticModel and runs.

        Dwave's LeapHybridCQMSampler. Note here that the supported type of
        decision variables is only Binary when using LeapHybridCQMSolver from
        Jijzept.

        To configure the solver, instantiate the `JijLeapHybridCQMParameters` class and pass the instance to the `parameters` argument.

        Args:
            model (jm.Problem): Optimization problem of JijModeling.
            feed_dict (dict[str, int | float | numpy.integer | numpy.floating | numpy.ndarray | list]): The actual values to be assigned to the placeholders.
            fixed_variables (Optional[dict[str, dict[tuple[int, ...], int]]]): variables to fix.
            relax_list (Optional[List[str]]): variable labels for continuous relaxation.
            parameters (Optional[JijLeapHybridCQMParameters]): Parameters used in Dwave Leap Hybrid CQMSampler. If `None`, the default value of the JijLeapHybridCQMParameters will be set.
            max_wait_time (int | float | None, optional): The number of timeout [sec] for post request. If `None`, 60 (one minute) will be set. Please note that this argument is for the `jijzept` timeout and not for configuring solver settings, such as solving time.
            sync (bool): Synchronous mode.
            queue_name (Optional[str]): Queue name.
            **kwargs: Dwave Leap parameters using **kwargs. If both `**kwargs` and `parameters` are exist, the value of `**kwargs` takes precedence.

        Returns:
            JijModelingSampleset: Stores samples and other information.

        Examples:
            ```python
            import jijmodeling as jm
            from jijzept import JijLeapHybridCQMSampler, JijLeapHybridCQMParameters

            w = jm.Placeholder("w", ndim=1)
            num_items = jm.Placeholder("num_items")
            c = jm.Placeholder("c")
            y = jm.BinaryVar("y", shape=(num_items,))
            x = jm.BinaryVar("x", shape=(num_items, num_items))
            i = jm.Element("i", belong_to=num_items)
            j = jm.Element("j", belong_to=num_items)
            problem = jm.Problem("bin_packing")
            problem += y[:].sum()
            problem += jm.Constraint("onehot_constraint", jm.sum(j, x[i, j]) - 1 == 0, forall=i)
            problem += jm.Constraint("knapsack_constraint", jm.sum(i, w[i] * x[i, j]) - y[j] * c <= 0, forall=j)
            feed_dict = {"num_items": 2, "w": [9, 1], "c": 10}

            sampler = JijLeapHybridCQMSampler(config="XX", token_leap="XX")
            parameters = JijLeapHybridCQMParameters(label="bin_packing")
            sampleset = sampler.sample_model(
                problem, feed_dict, parameters=parameters
            )
            ```
        """
        check_kwargs_against_dataclass(kwargs, JijLeapHybridCQMParameters)
        param_dict = merge_params_and_kwargs(
            parameters, kwargs, JijLeapHybridCQMParameters
        )
        param_dict["token"] = self.leap_token
        param_dict["url"] = self.leap_url

        para_search_params = ParameterSearchParameters(
            multipliers={},
            mul_search=False,
        )
        if fixed_variables is None:
            fixed_variables = {}
        if relax_list is None:
            relax_list = []

        if queue_name is None:
            queue_name = self.jijmodeling_solver_type.queue_name

        sample_set = sample_model(
            self.client,
            self.jijmodeling_solver_type.solver,
            queue_name=queue_name,
            problem=model,
            instance_data=feed_dict,
            fixed_variables=fixed_variables,
            parameter_search_parameters=para_search_params,
            max_wait_time=max_wait_time,
            sync=sync,
            relax_list=relax_list,
            **param_dict,
        )
        return sample_set

    def sample_instance(
        self,
        instance_id: str,
        fixed_variables: FixedVariables | None = None,
        relax_list: typ.List[str] | None = None,
        parameters: JijLeapHybridCQMParameters | None = None,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str | None = None,
        system_time: jm.SystemTime = jm.SystemTime(),
        **kwargs,
    ) -> JijModelingResponse:
        """Converts the uploaded instance to dimod.ConstrainedQuadraticModel and runs.

        Dwave's LeapHybridCQMSampler. Note here that the supported type of
        decision variables is only Binary when using LeapHybridCQMSolver from
        Jijzept.

        To configure the solver, instantiate the `JijLeapHybridCQMParameters` class and pass the instance to the `parameters` argument.

        Args:
            instance_id (str): The ID of the uploaded instance.
            fixed_variables (Optional[dict[str, dict[tuple[int, ...], int]]]): variables to fix.
            relax_list (Optional[List[str]]): variable labels for continuous relaxation.
            parameters (Optional[JijLeapHybridCQMParameters]): Parameters used in Dwave Leap Hybrid CQMSampler. If `None`, the default value of the JijLeapHybridCQMParameters will be set.
            max_wait_time (int | float | None, optional): The number of timeout [sec] for post request. If `None`, 60 (one minute) will be set. Please note that this argument is for the `jijzept` timeout and not for configuring solver settings, such as solving time.
            sync (bool): Synchronous mode.
            queue_name (Optional[str]): Queue name.
            system_time (jm.SystemTime): Object to store system times other than upload time.
            **kwargs: Dwave Leap parameters using **kwargs. If both `**kwargs` and `parameters` are exist, the value of `**kwargs` takes precedence.

        Returns:
            JijModelingSampleset: Stores samples and other information.

        Examples:
            ```python
            import jijmodeling as jm
            from jijzept import JijLeapHybridCQMSampler, JijLeapHybridCQMParameters

            w = jm.Placeholder("w", ndim=1)
            num_items = jm.Placeholder("num_items")
            c = jm.Placeholder("c")
            y = jm.BinaryVar("y", shape=(num_items,))
            x = jm.BinaryVar("x", shape=(num_items, num_items))
            i = jm.Element("i", belong_to=num_items)
            j = jm.Element("j", belong_to=num_items)
            problem = jm.Problem("bin_packing")
            problem += y[:].sum()
            problem += jm.Constraint("onehot_constraint", jm.sum(j, x[i, j]) - 1 == 0, forall=i)
            problem += jm.Constraint("knapsack_constraint", jm.sum(i, w[i] * x[i, j]) - y[j] * c <= 0, forall=j)
            feed_dict = {"num_items": 2, "w": [9, 1], "c": 10}

            sampler = JijLeapHybridCQMSampler(config="XX", token_leap="XX")
            parameters = JijLeapHybridCQMParameters(label="bin_packing")

            # upload instance
            instance_id = sampler.upload_instance(problem, feed_dict)

            # sample instance
            sampleset = sampler.sample_instance(instance_id, parameters=parameters)
            ```
        """

        check_kwargs_against_dataclass(kwargs, JijLeapHybridCQMParameters)
        param_dict = merge_params_and_kwargs(
            parameters, kwargs, JijLeapHybridCQMParameters
        )
        param_dict["token"] = self.leap_token
        param_dict["url"] = self.leap_url

        para_search_params = ParameterSearchParameters(
            multipliers={},
            mul_search=False,
        )
        if fixed_variables is None:
            fixed_variables = {}
        if relax_list is None:
            relax_list = []

        if queue_name is None:
            queue_name = self.jijmodeling_solver_type.queue_name

        sample_set = sample_instance(
            client=self.client,
            solver=self.jijmodeling_solver_type.solver,
            queue_name=queue_name,
            instance_id=instance_id,
            fixed_variables=fixed_variables,
            parameter_search_parameters=para_search_params,
            max_wait_time=max_wait_time,
            sync=sync,
            relax_list=relax_list,
            system_time=system_time,
            **param_dict,
        )
        return sample_set
