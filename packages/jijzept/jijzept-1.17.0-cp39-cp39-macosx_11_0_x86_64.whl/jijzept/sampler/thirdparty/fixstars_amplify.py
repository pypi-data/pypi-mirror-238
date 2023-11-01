from __future__ import annotations

from dataclasses import dataclass

import jijmodeling as jm

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


@dataclass
class JijFixstarsAmplifyParameters:
    """Manage Parameters for using Fixstars Amplify.

    Attributes:
        amplify_timeout (int): Set the timeout in milliseconds. Defaults to 1000.
        num_gpus (int): Set the number of GPUs to be used. The maximum number of GPUs available depends on the subscription plan, and 0 means the maximum number available. Defaults to 1.
        penalty_calibration (bool): Set whether to enable the automatic adjustment of the penalty function's multipliers. If multiplier is not set, it will be set true. Defaults to False.
        duplicate (bool): If True, all solutions with the same energy and the same feasibility are output. Otherwise, only one solution with the same energy and feasibility is output.
        num_outputs (int): The number of solutions to be output which have different energies and feasibility. Assumed 1 if no value is set. If set to 0, all the solutions are output. Defaults to 1.
    """

    amplify_timeout: int = 1000
    num_gpus: int = 1
    penalty_calibration: bool = False
    duplicate: bool = False
    num_outputs: int = 1


class JijFixstarsAmplifySampler(JijZeptBaseSampler):
    """Sampler using Fixstars Amplify."""

    jijmodeling_solver_type: SolverType = SolverType(
        queue_name="thirdpartysolver", solver="FixstarsAmplify"
    )

    def __init__(
        self,
        token: str | None = None,
        url: str | dict | None = None,
        proxy: str | None = None,
        config: str | None = None,
        config_env: str = "default",
        fixstars_token: str | None = None,
        fixstars_url: str | None = None,
    ) -> None:
        """Sets Jijzept token and url and fixstars amplify token and url.

        If `fixstars_token` and 'fixstars_url` are not specified in the arguments,
        JijZept configuration file is used.
        If `fixstars_token` and `fixstars_url` are specified in the arguments,
        that will be used as priority setting.

        Args:
            token (Optional[str]): Token string.
            url (Union[str, dict]): API URL.
            proxy (Optional[str]): Proxy URL.
            config (Optional[str]): Config file path for JijZept.
            config_env (str): config env.
            fixstars_token (Optional[str]): Token string for Fixstars Amplify.
            fixstars_url (Optional[str]): Url string for Fixstars Ampplify.

        raises:
            ConfigError: if `fixstars_token` is not defined in the argument or config.toml.
        """
        super().__init__(token, url, proxy, config, config_env)

        if fixstars_token is None:
            if "fixstars_token" in self.client.config.additional_setting:
                self.fixstars_token = self.client.config.additional_setting[
                    "fixstars_token"
                ]
            else:
                raise ConfigError(
                    "`fixstars_token` should be set in the argument or config file"
                )
        else:
            self.fixstars_token = fixstars_token

        if fixstars_url is None:
            if "fixstars_url" in self.client.config.additional_setting:
                self.fixstars_url = self.client.config.additional_setting[
                    "fixstars_url"
                ]
            else:
                self.fixstars_url = ""
        else:
            self.fixstars_url = fixstars_url

    def sample_model(
        self,
        model: jm.Problem,
        feed_dict: InstanceData,
        multipliers: dict[str, int | float] = {},
        fixed_variables: FixedVariables = {},
        parameters: JijFixstarsAmplifyParameters | None = None,
        normalize_qubo: bool = False,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str | None = None,
        needs_square_constraints: dict[str, bool] | None = None,
        relax_as_penalties: dict[str, bool] | None = None,
        **kwargs,
    ) -> JijModelingResponse:
        """Converts the given problem to amplify.BinaryQuadraticModel and run.

        Fixstars Amplify Solver. Note here that the supported type of decision
        variables is only Binary when using Fixstars Ampplify Solver from
        Jijzept.

        To configure the solver, instantiate the `JijFixstarsAmplifyParameters` class and pass the instance to the `parameters` argument.

        Args:
            model (jm.Problem): Mathematical expression of JijModeling.
            feed_dict (dict[str, int | float | numpy.integer | numpy.floating | numpy.ndarray | list]): The actual values to be assigned to the placeholders.
            multipliers (dict[str, Number]): The actual multipliers for penalty terms, derived from constraint conditions.
            fixed_variables (dict[str, dict[tuple[int, ...], int]]): Dictionary of variables to fix.
            parameters (Optional[JijFixstarsAmplifyParameters]): Parameters used in Fixstars Amplify. If `None`, the default value of the JijFixstarsAmplifyParameters will be set.
            normalize_qubo (bool): Option to normalize the QUBO coefficient. Defaults to `False`.
            max_wait_time (int | float | None, optional): The number of timeout [sec] for post request. If `None`, 60 (one minute) will be set. Please note that this argument is for the `jijzept` timeout and not for configuring solver settings, such as solving time.
            sync (bool): Synchronous mode.
            queue_name (Optional[str]): Queue name.
            needs_square_constraints (Optional[dict[str, bool]], optional): This dictionary object is utilized to determine whether to square the constraint condition while incorporating it into the QUBO/HUBO penalty term. Here, the constraint's name is used as the key. If the value is set to True, the corresponding constraint is squared upon its addition to the QUBO/HUBO penalty term. By default, the value is set to True for linear constraints, and to False for non-linear ones.
            relax_as_penalties (Optional[dict[str, bool]], optional): This dictionary object is designed to regulate the incorporation of constraint conditions into the QUBO/HUBO penalty term, with the constraint's name functioning as the key. If the key's value is True, the respective constraint is added to the QUBO/HUBO penalty term. If the value is False, the constraint is excluded from the penalty term, though it remains subject to evaluation to verify if it meets the constraint conditions. By default, all constraint conditions have this value set to True.
            **kwargs: Fixstars Amplify parameters using **kwargs. If both `**kwargs` and `parameters` are exist, the value of `**kwargs` takes precedence.

        Returns:
            Union[DimodResponse, JijModelingResponse]: Stores samples and other information.

        Examples:
            ```python
            import jijmodeling as jm
            from jijzept import JijFixstarsAmplifySampler, JijFixstarsAmplifyParameters

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
            multipliers = {"onehot_constraint": 11, "knapsack_constraint": 22}

            sampler = JijFixstarsAmplifySampler(config="xx", fixstars_token="oo")
            parameters = JijFixstarsAmplifyParameters(amplify_timeout=1000, num_outputs=1, filter_solution=False,
            penalty_calibration=False)
            sampleset = sampler.sample_model(
                problem, feed_dict, multipliers, parameters=parameters
            )
            ```
        """
        check_kwargs_against_dataclass(kwargs, JijFixstarsAmplifyParameters)
        param_dict = merge_params_and_kwargs(
            parameters, kwargs, JijFixstarsAmplifyParameters
        )

        para_search_params = ParameterSearchParameters(
            multipliers=multipliers,
            mul_search=False,
        )

        if queue_name is None:
            queue_name = self.jijmodeling_solver_type.queue_name

        param_dict["token"] = self.fixstars_token
        param_dict["url"] = self.fixstars_url
        param_dict["normalize_qubo"] = normalize_qubo
        param_dict["needs_square_constraints"] = needs_square_constraints
        param_dict["relax_as_penalties"] = relax_as_penalties
        max_wait_time = (
            param_dict["parameters"].pop("amplify_timeout")
            if max_wait_time is None
            else max_wait_time
        )

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
        multipliers: dict[str, int | float] = {},
        fixed_variables: FixedVariables = {},
        parameters: JijFixstarsAmplifyParameters | None = None,
        normalize_qubo: bool = False,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str | None = None,
        needs_square_constraints: dict[str, bool] | None = None,
        relax_as_penalties: dict[str, bool] | None = None,
        system_time: jm.SystemTime = jm.SystemTime(),
        **kwargs,
    ) -> JijModelingResponse:
        """Converts the uploaded instance to amplify.BinaryQuadraticModel and run.

        Fixstars Amplify Solver. Note here that the supported type of decision
        variables is only Binary when using Fixstars Ampplify Solver from
        Jijzept.

        To configure the solver, instantiate the `JijFixstarsAmplifyParameters` class and pass the instance to the `parameters` argument.

        Args:
            instance_id (str): The ID of the uploaded instance.
            multipliers (dict[str, Number]): The actual multipliers for penalty terms, derived from constraint conditions.
            fixed_variables (dict[str, dict[tuple[int, ...], int]]): Dictionary of variables to fix.
            parameters (Optional[JijFixstarsAmplifyParameters]): Parameters used in Fixstars Amplify. If `None`, the default value of the JijFixstarsAmplifyParameters will be set.
            normalize_qubo (bool): Option to normalize the QUBO coefficient. Defaults to `False`.
            max_wait_time (int | float | None, optional): The number of timeout [sec] for post request. If `None`, 60 (one minute) will be set. Please note that this argument is for the `jijzept` timeout and not for configuring solver settings, such as solving time.
            sync (bool): Synchronous mode.
            queue_name (Optional[str]): Queue name.
            needs_square_constraints (Optional[dict[str, bool]], optional): This dictionary object is utilized to determine whether to square the constraint condition while incorporating it into the QUBO/HUBO penalty term. Here, the constraint's name is used as the key. If the value is set to True, the corresponding constraint is squared upon its addition to the QUBO/HUBO penalty term. By default, the value is set to True for linear constraints, and to False for non-linear ones.
            relax_as_penalties (Optional[dict[str, bool]], optional): This dictionary object is designed to regulate the incorporation of constraint conditions into the QUBO/HUBO penalty term, with the constraint's name functioning as the key. If the key's value is True, the respective constraint is added to the QUBO/HUBO penalty term. If the value is False, the constraint is excluded from the penalty term, though it remains subject to evaluation to verify if it meets the constraint conditions. By default, all constraint conditions have this value set to True.
            system_time (jm.SystemTime): Object to store system times other than upload time.
            **kwargs: Fixstars Amplify parameters using **kwargs. If both `**kwargs` and `parameters` are exist, the value of `**kwargs` takes precedence.

        Returns:
            Union[DimodResponse, JijModelingResponse]: Stores samples and other information.

        Examples:
            ```python
            import jijmodeling as jm
            from jijzept import JijFixstarsAmplifySampler, JijFixstarsAmplifyParameters

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
            multipliers = {"onehot_constraint": 11, "knapsack_constraint": 22}

            sampler = JijFixstarsAmplifySampler(config="xx", fixstars_token="oo")
            parameters = JijFixstarsAmplifyParameters(
                amplify_timeout=1000,
                num_outputs=1,
                filter_solution=False,
                penalty_calibration=False
            )

            # upload instance
            instance_id = sampler.upload_instance(problem, feed_dict)

            # sample instance
            sampleset = sampler.sample_model(
                instance_id, multipliers, parameters=parameters
            )
            ```
        """
        check_kwargs_against_dataclass(kwargs, JijFixstarsAmplifyParameters)
        param_dict = merge_params_and_kwargs(
            parameters, kwargs, JijFixstarsAmplifyParameters
        )

        para_search_params = ParameterSearchParameters(
            multipliers=multipliers,
            mul_search=False,
        )

        if queue_name is None:
            queue_name = self.jijmodeling_solver_type.queue_name

        param_dict["token"] = self.fixstars_token
        param_dict["url"] = self.fixstars_url
        param_dict["normalize_qubo"] = normalize_qubo
        param_dict["needs_square_constraints"] = needs_square_constraints
        param_dict["relax_as_penalties"] = relax_as_penalties
        max_wait_time = (
            param_dict["parameters"].pop("amplify_timeout")
            if max_wait_time is None
            else max_wait_time
        )

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
