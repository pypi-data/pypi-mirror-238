from __future__ import annotations

import dataclasses

from typing import Literal

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
class JijVectorAnnealingParameters:
    """Parameters for JijVectorAnnealingSampler.

    Args:
        num_reads (int, optional): Number of reads. Defaults to None.
        num_results (int, optional): Number of results. Defaults to None.
        num_sweeps (int, optional): Number of sweeps. Defaults to None.
        beta_range (list, optional): Beta range. Defaults to None.
        beta_list (list[float], optional): Beta list. Defaults to None.
        init_spin (dict[str, int], optional): Initial spin. Defaults to None.
        dense (bool, optional): Dense. Defaults to None.
        num_threads (int, optional): Number of threads. Defaults to None.
        vector_mode (Literal["speed", "accuracy"], optional): Vector mode. Defaults to None.
        timeout (int, optional): Timeout. Defaults to None.
        needs_square_constraints (dict[str, bool], optional): Needs square constraints. Defaults to None.
        relax_as_penalties (dict[str, bool], optional): Relax as penalties. Defaults to None.
    """

    num_reads: int | None = None
    num_results: int | None = None
    num_sweeps: int | None = None
    beta_range: list | None = None
    beta_list: list[float] | None = None
    init_spin: dict[str, int] | None = None
    dense: bool | None = None
    num_threads: int | None = None
    vector_mode: Literal["speed", "accuracy"] | None = None
    timeout: int | None = None
    needs_square_constraints: dict[str, bool] | None = None
    relax_as_penalties: dict[str, bool] | None = None


class JijVectorAnnealingSampler(JijZeptBaseSampler):
    """Sampler using SX-Aurora Vector Annealing."""

    jijmodeling_solver_type = SolverType(
        queue_name="vectorannealingsolver", solver="VectorAnnealing"
    )

    def sample_model(
        self,
        problem: jm.Problem,
        feed_dict: InstanceData,
        multipliers: dict[str, int | float] = {},
        fixed_variables: FixedVariables = {},
        search: bool = False,
        num_search: int = 15,
        algorithm: str | None = None,
        parameters: JijVectorAnnealingParameters | None = None,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str | None = None,
        **kwargs,
    ) -> JijModelingResponse:
        """Sample using JijModeling by means of Jij SX-Aurora Annealing solver.

        To configure the solver, instantiate the `JijVectorAnnealingParameters` class and pass the instance to the `parameters` argument.

        Args:
            problem (jm.Problem): Mathematical expression of JijModeling.
            feed_dict (dict[str, int | float | numpy.integer | numpy.floating | numpy.ndarray | list]): The actual values to be assigned to the placeholders.
            multipliers (Dict[str, Number], optional): The actual multipliers for penalty terms, derived from constraint conditions.
            fixed_variables (dict[str, dict[tuple[int, ...], int]]): dictionary of variables to fix.
            search (bool, optional): If `True`, the parameter search will be carried out, which tries to find better values of multipliers for penalty terms.
            num_search (int, optional): The number of parameter search iteration. Defaults to set 15. This option works if `search` is `True`.
            algorithm (Optional[str], optional): Algorithm for parameter search. Defaults to None.
            parameters (Optional[JijVectorAnnealingParameters], optional): parameters for SXAurora. Defaults to None.
            max_wait_time (int | float | None, optional): The number of timeout [sec] for post request. If `None`, 60 (one minute) will be set. Please note that this argument is for the `jijzept` timeout and not for configuring solver settings, such as solving time.
            sync (bool, optional): Synchronous mode.
            queue_name (Optional[str], optional): Queue name.
            **kwargs: VectorAnnealing parameters using **kwargs. If both `**kwargs` and `parameters` are exist, the value of `**kwargs` takes precedence.

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

            sampler = jz.JijVectorAnnealingSampler(config='config.toml')
            response = sampler.sample_model(problem, {'n': 5, 'd': [1,2,3,4,5]})
            ```
        """
        check_kwargs_against_dataclass(kwargs, JijVectorAnnealingParameters)
        param_dict = merge_params_and_kwargs(
            parameters, kwargs, JijVectorAnnealingParameters
        )

        para_search_params = ParameterSearchParameters(
            multipliers=multipliers,
            mul_search=search,
            num_search=num_search,
            algorithm=algorithm,
        )

        if queue_name is None:
            queue_name = self.jijmodeling_solver_type.queue_name

        sample_set = sample_model(
            self.client,
            self.jijmodeling_solver_type.solver,
            queue_name=queue_name,
            problem=problem,
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
        search: bool = False,
        num_search: int = 15,
        algorithm: str | None = None,
        parameters: JijVectorAnnealingParameters | None = None,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str | None = None,
        system_time: jm.SystemTime = jm.SystemTime(),
        **kwargs,
    ) -> JijModelingResponse:
        """Sample using the uploaded instance by means of Jij SX-Aurora Annealing solver.

        To configure the solver, instantiate the `JijVectorAnnealingParameters` class and pass the instance to the `parameters` argument.

        Args:
            instance_id (str): The ID of the upload instance.
            multipliers (Dict[str, Number], optional): The actual multipliers for penalty terms, derived from constraint conditions.
            fixed_variables (dict[str, dict[tuple[int, ...], int]]): dictionary of variables to fix.
            search (bool, optional): If `True`, the parameter search will be carried out, which tries to find better values of multipliers for penalty terms.
            num_search (int, optional): The number of parameter search iteration. Defaults to set 15. This option works if `search` is `True`.
            algorithm (Optional[str], optional): Algorithm for parameter search. Defaults to None.
            parameters (Optional[JijVectorAnnealingParameters], optional): parameters for SXAurora. Defaults to None.
            max_wait_time (int | float | None, optional): The number of timeout [sec] for post request. If `None`, 60 (one minute) will be set. Please note that this argument is for the `jijzept` timeout and not for configuring solver settings, such as solving time.
            sync (bool, optional): Synchronous mode.
            queue_name (Optional[str], optional): Queue name.
            system_time (jm.SystemTime): Object to store system times other than upload time.
            **kwargs: VectorAnnealing parameters using **kwargs. If both `**kwargs` and `parameters` are exist, the value of `**kwargs` takes precedence.

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

            # initialize sampler
            sampler = jz.JijVectorAnnealingSampler(config='config.toml')

            # upload instance
            instance_id = sampler.upload_instance(problem, {'n': 5, 'd': [1,2,3,4,5]})

            # sample instance
            sample_set = sampler.sample_instance(instance_id)
            ```
        """
        check_kwargs_against_dataclass(kwargs, JijVectorAnnealingParameters)
        param_dict = merge_params_and_kwargs(
            parameters, kwargs, JijVectorAnnealingParameters
        )

        para_search_params = ParameterSearchParameters(
            multipliers=multipliers,
            mul_search=search,
            num_search=num_search,
            algorithm=algorithm,
        )

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
            system_time=system_time,
            **param_dict,
        )
        return sample_set
