from __future__ import annotations

from dataclasses import dataclass

import jijmodeling as jm

from jijzept.entity.schema import SolverType
from jijzept.exception import ConfigError
from jijzept.response.jmresponse import JijModelingResponse
from jijzept.sampler.base_sampler import (
    JijZeptBaseSampler,
    ParameterSearchParameters,
    check_kwargs_against_dataclass,
    merge_params_and_kwargs,
    sample_instance,
    sample_model,
)
from jijzept.type_annotation import FixedVariables, InstanceData


@dataclass
class JijDA4SolverParameters:
    """Manage Parameters for using fourth generation Digital Annealer.

    Attributes:
        time_limit_sec (int): Set the timeout in seconds in the range 1 ~ 1800.
        target_energy (Optional[float]): Set the target energy value. The calculation is terminated when the minimum energy savings reaches the target energy.
        num_run (int): Set the number of parallel trial iterations in the range 1 ~ 16.
        num_group (int): Set the number of groups of parallel trials in the range 1 ~ 16.
        num_output_solution (int): Set the number of output solutions for each parallel trial group in the range 1 ~ 1024.
        gs_level (int): Set the level of global search. The higher this value, the longer the constraint utilization search will search in the range 0 ~ 100. If set the 1way 1hot or 2way 1hot, it is recommended that 0 be set for gs_level.
        gs_cutoff (int): Set the convergence decision level in the constraint utilization search of the solver in the range 0 ~ 1000000. If `0`, convergence judgement is off.
        one_hot_level (int): Levels of 1hot constraints search.
        one_hot_cutoff (int): Convergence decision level for 1hot constraints search. If 0 is set, this function is turned off.
        internal_penalty (int): 1hot constraint internal generation mode. Note that if 1way- or 2way 1hot constraints are specified to `jijmodeling.Constraint`, internal_penalty is set to 1 internally, regardless of user input.
        penalty_auto_mode (int): Set the coefficient adjustment mode for the constaint term. If `0`, fixed to the value setin `penlaty_coef`. If `1`, the value set in `penalty_coef` is used as the initial value and adjusted automatically.
        penalty_coef (int): Set the coefficients of the constraint term.
        penalty_inc_rate (int): Set parameters for automatic adjustment of constriant term.
        max_penalty_coef (int): Set the maximum value of the constraint term coefficient in the global search. If no maximum value is specified, set to 0.
    """

    time_limit_sec: int = 10
    target_energy: float | None = None
    num_run: int = 16
    num_group: int = 1
    num_output_solution: int = 5
    gs_level: int = 5
    gs_cutoff: int = 8000
    one_hot_level: int = 3
    one_hot_cutoff: int = 100
    internal_penalty: int = 0
    penalty_auto_mode: int = 1
    penalty_coef: int = 1
    penalty_inc_rate: int = 150
    max_penalty_coef: int = 0


class JijDA4Sampler(JijZeptBaseSampler):
    """Sampler using Digital Annealer v4."""

    jijmodeling_solver_type: SolverType = SolverType(
        queue_name="da4solver",
        solver="DigitalAnnealerV4",
    )

    def __init__(
        self,
        token: str | None = None,
        url: str | None = None,
        proxy: str | None = None,
        config: str | None = None,
        config_env: str = "default",
        da4_token: str | None = None,
        da4_url: str | None = None,
    ) -> None:
        """Sets Jijzept token and url and fourth generation Digital Annealer token and url.

        If `da4_token` and 'da4_url` are not specified in the arguments,
        JijZept configuration file is used.
        If `da4_token` and `da4_url` are specified in the arguments,
        that will be used as priority setting.

        Args:
            token (Optional[str]): Token string.
            url (Optional[Union[str, dict]]): API URL.
            proxy (Optional[str]): Proxy URL.
            config (Optional[str]): Config file path for JijZept.
            config_env (str): config env.
            da4_token (Optional[str]): Token string for Degital Annealer 4.
            da4_url (Optional[str]): API Url string for Degital Annealer 4.

        raises:
            ConfigError: if `da4_token` is not defined in the argument or config.toml.
        """
        super().__init__(
            token=token, url=url, proxy=proxy, config=config, config_env=config_env
        )

        if da4_token is None:
            if "da4_token" in self.client.config.additional_setting:
                self.da4_token = self.client.config.additional_setting["da4_token"]
            else:
                raise ConfigError(
                    "`da4_token` should be set in the argument or config file."
                )
        else:
            self.da4_token = da4_token

        if da4_url is None:
            if "da4_url" in self.client.config.additional_setting:
                self.da4_url = self.client.config.additional_setting["da4_url"]
            else:
                self.da4_url = "https://api.aispf.global.fujitsu.com/da"
        else:
            self.da4_url = da4_url

    def sample_model(
        self,
        model: jm.Problem,
        feed_dict: InstanceData,
        fixed_variables: FixedVariables = {},
        inequalities_lambda: dict[str, int] = {},
        parameters: JijDA4SolverParameters | None = None,
        normalize_qubo: bool = False,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str | None = None,
        **kwargs,
    ) -> JijModelingResponse:
        """Sample using JijModeling by means of fourth generation Digital Annealer.

        Note that this sampler solve problems with using Azure Blob Storage, which is a feature of Digital Annealer
        v4, and there is no option not to use Azure Blob Storage.

        To configure the solver, instantiate the `JijDA4SolverParameters` class and pass the instance to the `parameters` argument.

        Args:
            model (jm.Problem): Mathematical expression of JijModeling.
            feed_dict (dict[str, int | float | numpy.integer | numpy.floating | numpy.ndarray | list]): The actual values to be assigned to the placeholders.
            fixed_variables (dict[str, dict[tuple[int, ...], int]]): Dictionary of variables to fix.
            inequalities_lambda (dict[str, int]): Coefficient of inequality. If omitted, set to 1. The coefficients of the equality constraints can be set from JijDA4SolverParameters.
            parameters (Optional[JijDA4SolverParameters]): Parameters used in Ditital Annealer 4. If `None`, the default value of the JijDA4SolverParameters will be set.
            normalize_qubo (bool): Option to normalize the QUBO coefficient and inequality constraint conditions. Defaults to `False`.
            max_wait_time (int | float | None, optional): The number of timeout [sec] for post request. If `None`, 60 (one minute) will be set. Please note that this argument is for the `jijzept` timeout and not for configuring solver settings, such as solving time.
            sync (bool): Synchronous mode.
            queue_name (Optional[str]): Queue name.
            **kwargs: Digital Annealer 4 parameters using **kwargs. If both `**kwargs` and `parameters` are exist, the value of `**kwargs` takes precedence.

        Returns:
            JijModelingResponse: Stores minimum energy samples and other information.

        Examples:
            ```python
            import jijmodeling as jm
            from jijzept import JijDA4Sampler, JijDA4SolverParameters

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
            problem += jm.Constraint(
                "knapsack_constraint", jm.sum(i, w[i] * x[i, j]) - y[j] * c <= 0, forall=j
            )

            feed_dict = {"num_items": 2, "w": [9, 1], "c": 10}
            inequalities_lambda = {"knapsack_constraint": 22}

            sampler = JijDA4Sampler(config="xx", da4_token="oo")
            parameters = JijDA4SolverParameters(penalty_coef=2)

            sampleset = sampler.sample_model(
                problem, feed_dict, inequalities_lambda=inequalities_lambda, parameters=parameters
            )
            ```
        """
        check_kwargs_against_dataclass(kwargs, JijDA4SolverParameters)
        param_dict = merge_params_and_kwargs(parameters, kwargs, JijDA4SolverParameters)

        para_search_params = ParameterSearchParameters(
            multipliers={},
            mul_search=False,
        )

        if queue_name is None:
            queue_name = self.jijmodeling_solver_type.queue_name

        param_dict["token"] = self.da4_token
        param_dict["url"] = self.da4_url
        param_dict["normalize_qubo"] = normalize_qubo
        param_dict["inqualities_lambda"] = inequalities_lambda

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
            **param_dict,
        )
        return sample_set

    def sample_instance(
        self,
        instance_id: str,
        fixed_variables: FixedVariables = {},
        inequalities_lambda: dict[str, int] = {},
        parameters: JijDA4SolverParameters | None = None,
        normalize_qubo: bool = False,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str | None = None,
        system_time: jm.SystemTime = jm.SystemTime(),
        **kwargs,
    ) -> JijModelingResponse:
        """Sample using the uploaded instance by means of fourth generation Digital Annealer.

        Note that this sampler solve problems with using Azure Blob Storage, which is a feature of Digital Annealer
        v4, and there is no option not to use Azure Blob Storage.

        To configure the solver, instantiate the `JijDA4SolverParameters` class and pass the instance to the `parameters` argument.

        Args:
            instance_id (str): The ID of the uploaded instance.
            fixed_variables (dict[str, dict[tuple[int, ...], int]]): Dictionary of variables to fix.
            inequalities_lambda (dict[str, int]): Coefficient of inequality. If omitted, set to 1. The coefficients of the equality constraints can be set from JijDA4SolverParameters.
            parameters (Optional[JijDA4SolverParameters]): Parameters used in Ditital Annealer 4. If `None`, the default value of the JijDA4SolverParameters will be set.
            normalize_qubo (bool): Option to normalize the QUBO coefficient and inequality constraint conditions. Defaults to `False`.
            max_wait_time (int | float | None, optional): The number of timeout [sec] for post request. If `None`, 60 (one minute) will be set. Please note that this argument is for the `jijzept` timeout and not for configuring solver settings, such as solving time.
            sync (bool): Synchronous mode.
            queue_name (Optional[str]): Queue name.
            system_time (jm.SystemTime): Object to store system times other than upload time.
            **kwargs: Digital Annealer 4 parameters using **kwargs. If both `**kwargs` and `parameters` are exist, the value of `**kwargs` takes precedence.

        Returns:
            JijModelingResponse: Stores minimum energy samples and other information.

        Examples:
            ```python
            import jijmodeling as jm
            from jijzept import JijDA4Sampler, JijDA4SolverParameters

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
            problem += jm.Constraint(
                "knapsack_constraint", jm.sum(i, w[i] * x[i, j]) - y[j] * c <= 0, forall=j
            )

            feed_dict = {"num_items": 2, "w": [9, 1], "c": 10}
            inequalities_lambda = {"knapsack_constraint": 22}

            sampler = JijDA4Sampler(config="xx", da4_token="oo")
            parameters = JijDA4SolverParameters(penalty_coef=2)

            # upload instance
            instance_id = sampler.upload_instance(problem, feed_dict)

            # sample instance
            sampleset = sampler.sample_instance(
                instance_id, inequalities_lambda=inequalities_lambda, parameters=parameters
            )
            ```
        """
        check_kwargs_against_dataclass(kwargs, JijDA4SolverParameters)
        param_dict = merge_params_and_kwargs(parameters, kwargs, JijDA4SolverParameters)

        para_search_params = ParameterSearchParameters(
            multipliers={},
            mul_search=False,
        )

        if queue_name is None:
            queue_name = self.jijmodeling_solver_type.queue_name

        param_dict["token"] = self.da4_token
        param_dict["url"] = self.da4_url
        param_dict["normalize_qubo"] = normalize_qubo
        param_dict["inqualities_lambda"] = inequalities_lambda

        sample_set = sample_instance(
            client=self.client,
            solver=self.jijmodeling_solver_type.solver,
            queue_name=queue_name,
            instance_id=instance_id,
            fixed_variables=fixed_variables,
            parameter_search_parameters=para_search_params,
            max_wait_time=max_wait_time,
            sync=sync,
            system_time=system_time,
            **param_dict,
        )
        return sample_set
