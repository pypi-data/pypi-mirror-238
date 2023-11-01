from __future__ import annotations

import dataclasses, warnings

import jijmodeling as jm

from jijzept.entity.schema import SolverType
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


@dataclasses.dataclass
class JijSQBMParameters:
    """Manage Parameters for using Toshiba Simulated Bifurcation Machine.

    An parameter with none will be set to the default value in Simulated Bifurcation Machine.
    For more information on the parameters. Please see [this page](https://learn.microsoft.com/ja-jp/azure/quantum/provider-toshiba).

    Attributes:
        steps (Optional[int]): Specifies the number of steps in a computation request. The value 0 (zero) means auto step where SQBM+ computation service dynamically determines the number of steps. The maximum is 100,000,000.
        loops (Optional[int]): Specifies the number of loops in SQBM+ computation. SQBM+ computation service searches for a better solution while repeating loops as many times as is specified. If 0 (zero) is specified, computation will be repeated until a timeout occurs. The maximum is 10,000,000.
        timeout (Optional[float]): Specifies the maximum computation time (timeout) in seconds. When the computation time reaches the upper limit before completing the computation for steps x loops, the computation ends at that point. In this case, the execution result will be the best solution obtained thus far. If 0 is specified for the parameter loops, loops will be repeated until the time specified by the parameter timeout expires. The maximum is 3600 and the minimum is 0.001.
        target (Optional[float]): Specifies the end condition of a computation request. When the evaluation value reaches this value, the computation will stop. If 0 is specified for the parameter loops, loops will be repeated either until the objective function reaches the value specified in the parameter target or until a timeout occurs.
        maxout (Optional[int]): Specifies the upper limit of the number of solutions to be outputted. Until the limit specified by maxout is reached, SQBM+ computation service outputs the obtained solutions in ascending order of the value of the objective function. The maximum is 1,000.
        dt (Optional[float]): Specifies the time per step. The range of the value is greater than 0.0 and less than or equal to 1.0.
        C (Optional[float]): Corresponds to the constant ξ0, appearing in the paper by Goto, Tatsumura, & Dixon (2019, p. 2), which is the theoretical basis of SQBM+. Specify the constant as a single-precision floating point number, equal to or more than 0. If the value is 0, the value C is automatically determined.
        algo (Optional[str]): Specifies the type of SQBM+ computation algorithm. One of "1.5" (bSB algorithm) or "2.0" (dSB algorithm) (see note below for details). Depending on the type of problem, there may be differences in performance between the "1.5" and "2.0" algorithms. Try both and decide which yields better performance.
        auto (Optional[bool]): Specifies the parameter auto tuning flag. If the value is "true," SQBM+ computation service searches for the values of the parameters automatically to obtain the best solution. Parameters other than auto are treated as follows in this case. algo and dt are ignored and tuned automatically. loops and maxout are ignored. timeout can be specified as the total computation time (sec). Other parameters are treated as defined.
    """

    steps: int | None = None
    loops: int | None = None
    timeout: float | None = None
    target: float | None = None
    maxout: int | None = None
    dt: float | None = None
    C: float | None = None
    algo: str | None = None
    auto: bool | None = None


class JijSQBMSampler(JijZeptBaseSampler):
    solver_type = SolverType(queue_name="qiosolver", solver="SQBM+")
    jijmodeling_solver_type = SolverType(
        queue_name="qiosolver", solver="SQBM+ParaSearch"
    )

    def sample_model(
        self,
        model: jm.Problem,
        feed_dict: InstanceData,
        multipliers: dict[str, int | float] | None = None,
        fixed_variables: FixedVariables | None = None,
        needs_square_dict: dict[str, bool] | None = None,
        search: bool = False,
        num_search: int = 15,
        algorithm: str | None = None,
        parameters: JijSQBMParameters | None = None,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str | None = None,
        **kwargs,
    ) -> JijModelingResponse:
        """Sample using JijModeling by means of Toshiba Simulated Bifurcation Machine solver.

        To configure the solver, instantiate the `JijSQBMParameters` class for your desired solver and pass the instance to the `parameters` argument.

        Args:
            model (jijmodeling.Problem): Mathematical model is constracted by JijModeling.
            feed_dict (dict[str, int | float | numpy.integer | numpy.floating | numpy.ndarray | list]): The actual values to be assigned to the placeholders.
            multipliers (Dict[str, Number], optional): The actual multipliers for penalty terms, derived from constraint conditions.
            fixed_variables (dict[str, dict[tuple[int, ...], int]]): dictionary of variables to fix.
            needs_square_dict (Dict[str, bool], optional): If `True`, the corresponding constraint is squared when added as a penalty to the QUBO. When the constraint label is not added to the 'needs_square_dict', it defaults to `True` for linear constraints and `False` for non-linear constraints.
            search (bool, optional): If `True`, the parameter search will be carried out, which tries to find better values of multipliers for penalty terms.
            num_search (int, optional): The number of parameter search iteration. Defaults to set 15. This option works if `search` is `True`.
            algorithm (Optional[str]): Algorithm for parameter search. Defaults to None.
            parameters (JijSQBMParameters | None, optional): parameters for SQBM+. Defaults to None.
            max_wait_time (int | float | None, optional): The number of timeout [sec] for post request. If `None`, 60 (one minute) will be set. Please note that this argument is for the `jijzept` timeout and not for configuring solver settings, such as solving time.
            sync (bool, optional): Synchronous mode.
            queue_name (Optional[str], optional): Queue name.
            **kwargs: SQBM+ parameters using **kwargs. If both `**kwargs` and `parameters` are exist, the value of `**kwargs` takes precedence.

        Returns:
            JijModelingResponse: Stores minimum energy samples and other information.

        Examples:
            ```python
            import jijzept as jz
            import jijmodeling as jm

            n = jm.Placeholder('n')
            x = jm.BinaryVar('x', shape=(n,))
            d = jm.Placeholder('d', ndim=1)
            i = jm.Element("i", belong_to=n)
            problem = jm.Problem('problem')
            problem += jm.sum(i, d[i] * x[i])

            sampler = jz.JijSQBMSampler(config='config.toml')
            response = sampler.sample_model(problem, feed_dict={'n': 5, 'd': [1,2,3,4,5]})
            ```
        """

        if multipliers is None:
            multipliers = {}
        if fixed_variables is None:
            fixed_variables = {}

        if needs_square_dict is not None:
            warnings.warn(
                message="The argument `needs_square_dict` is deprecated. Please don't use it.",
                stacklevel=2,
            )

        check_kwargs_against_dataclass(kwargs, JijSQBMParameters)
        param_dict = merge_params_and_kwargs(parameters, kwargs, JijSQBMParameters)

        if queue_name is None:
            queue_name = self.jijmodeling_solver_type.queue_name

        para_search_params = ParameterSearchParameters(
            multipliers=multipliers,
            mul_search=search,
            num_search=num_search,
            algorithm=algorithm,
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
        multipliers: dict[str, int | float] | None = None,
        fixed_variables: FixedVariables | None = None,
        search: bool = False,
        num_search: int = 15,
        algorithm: str | None = None,
        parameters: JijSQBMParameters | None = None,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str | None = None,
        system_time: jm.SystemTime = jm.SystemTime(),
        **kwargs,
    ) -> JijModelingResponse:
        """Sample using the uploaded instance by means of Toshiba Simulated Bifurcation Machine solver.

        To configure the solver, instantiate the `JijSQBMParameters` class for your desired solver and pass the instance to the `parameters` argument.

        Args:
            instance_id (str): The ID of the uploaded instance.
            multipliers (Dict[str, Number], optional): The actual multipliers for penalty terms, derived from constraint conditions.
            fixed_variables (dict[str, dict[tuple[int, ...], int]]): dictionary of variables to fix.
            search (bool, optional): If `True`, the parameter search will be carried out, which tries to find better values of multipliers for penalty terms.
            num_search (int, optional): The number of parameter search iteration. Defaults to set 15. This option works if `search` is `True`.
            algorithm (Optional[str]): Algorithm for parameter search. Defaults to None.
            parameters (JijSQBMParameters | None, optional): parameters for SQBM+. Defaults to None.
            max_wait_time (int | float | None, optional): The number of timeout [sec] for post request. If `None`, 60 (one minute) will be set. Please note that this argument is for the `jijzept` timeout and not for configuring solver settings, such as solving time.
            sync (bool, optional): Synchronous mode.
            queue_name (Optional[str], optional): Queue name.
            system_time (jm.SystemTime): Object to store system times other than upload time.
            **kwargs: SQBM+ parameters using **kwargs. If both `**kwargs` and `parameters` are exist, the value of `**kwargs` takes precedence.

        Returns:
            JijModelingResponse: Stores minimum energy samples and other information.

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
            sampler = jz.JijSQBMSampler(config='config.toml')

            # upload instance
            instance_id = sampler.upload_instance(problem, {'n': 5, 'd': [1,2,3,4,5]})

            # sample uploaded instance
            sample_set = sampler.sample_instance(instance_id)
            ```
        """
        if multipliers is None:
            multipliers = {}
        if fixed_variables is None:
            fixed_variables = {}

        check_kwargs_against_dataclass(kwargs, JijSQBMParameters)
        param_dict = merge_params_and_kwargs(parameters, kwargs, JijSQBMParameters)

        if queue_name is None:
            queue_name = self.jijmodeling_solver_type.queue_name

        para_search_params = ParameterSearchParameters(
            multipliers=multipliers,
            mul_search=search,
            num_search=num_search,
            algorithm=algorithm,
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
