from __future__ import annotations

import typing as typ
import warnings

from dataclasses import dataclass

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

T = typ.TypeVar("T")


@dataclass
class JijSAParameters:
    """Manage Parameters for using JijSASampler.

    Attributes:
        beta_min (Optional[float], optional): Minimum (initial) inverse temperature. If `None`, this will be set automatically.
        beta_max (Optional[float], optional): Maximum (final) inverse temperature. If `None`, this will be set automatically.
        num_sweeps (Optional[int], optional): The number of Monte-Carlo steps. If `None`, 1000 will be set.
        num_reads (Optional[int], optional): The number of samples. If `None`, 1 will be set.
        initial_state (Optional[dict], optional): Initial state. If `None`, this will be set automatically.
        updater (Optional[str], optional): Updater algorithm. "single spin flip" or "swendsen wang". If `None`, "single spin flip" will be set.
        sparse (Optional[bool], optional): If `True`, only non-zero matrix elements are stored, which will save memory. If `None`, `False` will be set.
        reinitialize_state (Optional[bool], optional): If `True`, reinitialize state for each run. If `None`, `True` will be set.
        seed (Optional[int], optional): Seed for Monte Carlo algorithm. If `None`, this will be set automatically.
        needs_square_constraints (Optional[dict[str, bool]], optional): This dictionary object is utilized to determine whether to square the constraint condition while incorporating it into the QUBO/HUBO penalty term. Here, the constraint's name is used as the key. If the value is set to True, the corresponding constraint is squared upon its addition to the QUBO/HUBO penalty term. By default, the value is set to True for linear constraints, and to False for non-linear ones.
        relax_as_penalties (Optional[dict[str, bool]], optional): This dictionary object is designed to regulate the incorporation of constraint conditions into the QUBO/HUBO penalty term, with the constraint's name functioning as the key. If the key's value is True, the respective constraint is added to the QUBO/HUBO penalty term. If the value is False, the constraint is excluded from the penalty term, though it remains subject to evaluation to verify if it meets the constraint conditions. By default, all constraint conditions have this value set to True.
    """

    beta_min: float | None = None
    beta_max: float | None = None
    num_sweeps: int | None = None
    num_reads: int | None = None
    initial_state: list | dict | None = None
    updater: str | None = None
    sparse: bool | None = None
    reinitialize_state: bool | None = None
    seed: int | None = None
    needs_square_constraints: dict[str, bool] | None = None
    relax_as_penalties: dict[str, bool] | None = None


class JijSASampler(JijZeptBaseSampler):
    """Simulated Annealing (SA) sampler.

    SA for QUBO and the Ising Model.
    This sampler is designed for verifying and testing models with small instances and is best suited for initial testing and exploration of your models.
    """

    solver_type = SolverType(queue_name="openjijsolver", solver="SA")
    hubo_solver_type = SolverType(queue_name="openjijsolver", solver="HUBOSA")
    jijmodeling_solver_type = SolverType(
        queue_name="openjijsolver", solver="SAParaSearch"
    )

    def sample_model(
        self,
        model: jm.Problem,
        feed_dict: InstanceData,
        multipliers: dict[str, int | float] = {},
        fixed_variables: FixedVariables = {},
        needs_square_dict: dict[str, bool] | None = None,
        search: bool = False,
        num_search: int = 15,
        algorithm: str | None = None,
        parameters: JijSAParameters | None = None,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str | None = None,
        **kwargs,
    ) -> JijModelingResponse:
        """Sample using JijModeling by means of the simulated annealing.

        To configure the solver, instantiate the `JijSAParameters` class and pass the instance to the `parameters` argument.

        Args:
            model (jm.Problem): Mathematical expression of JijModeling.
            feed_dict (dict[str, int | float | numpy.integer | numpy.floating | numpy.ndarray | list]): The actual values to be assigned to the placeholders.
            multipliers (Dict[str, Number], optional): The actual multipliers for penalty terms, derived from constraint conditions.
            fixed_variables (dict[str, dict[tuple[int, ...], int]]): dictionary of variables to fix.
            search (bool, optional): If `True`, the parameter search will be carried out, which tries to find better values of multipliers for penalty terms.
            num_search (int, optional): The number of parameter search iteration. Defaults to set 15. This option works if `search` is `True`.
            algorithm (Optional[str], optional): Algorithm for parameter search. Defaults to None.
            parameters (JijSAParameters | None, optional): defaults None.
            max_wait_time (int | float | None, optional): The number of timeout [sec] for post request. If `None`, 60 (one minute) will be set. Please note that this argument is for the `jijzept` timeout and not for configuring solver settings, such as solving time.
            sync (bool, optional): Synchronous mode.
            queue_name (Optional[str], optional): Queue name.
            **kwargs: SA parameters using **kwargs. If both `**kwargs` and `parameters` are exist, the value of `**kwargs` takes precedence.

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

            sampler = jz.JijSASampler(config='config.toml')
            response = sampler.sample_model(problem, feed_dict={'n': 5, 'd': [1,2,3,4,5]})
            ```
        """
        if needs_square_dict is not None:
            warnings.warn(
                message="The argument `needs_square_dict` is deprecated. Please don't use it.",
                stacklevel=2,
            )

        check_kwargs_against_dataclass(kwargs, JijSAParameters)
        param_dict = merge_params_and_kwargs(parameters, kwargs, JijSAParameters)

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
        search: bool = False,
        num_search: int = 15,
        algorithm: str | None = None,
        parameters: JijSAParameters | None = None,
        max_wait_time: int | float | None = None,
        sync: bool = True,
        queue_name: str | None = None,
        system_time: jm.SystemTime = jm.SystemTime(),
        **kwargs,
    ) -> JijModelingResponse:
        """Sample using the uploaded instance by means of the simulated annealing.

        To configure the solver, instantiate the `JijSAParameters` class and pass the instance to the `parameters` argument.

        Args:
            instance_id (str): The ID of the uploaded instance.
            multipliers (Dict[str, Number], optional): The actual multipliers for penalty terms, derived from constraint conditions.
            fixed_variables (dict[str, dict[tuple[int, ...], int]]): dictionary of variables to fix.
            search (bool, optional): If `True`, the parameter search will be carried out, which tries to find better values of multipliers for penalty terms.
            num_search (int, optional): The number of parameter search iteration. Defaults to set 15. This option works if `search` is `True`.
            algorithm (Optional[str], optional): Algorithm for parameter search. Defaults to None.
            parameters (JijSAParameters | None, optional): defaults None.
            max_wait_time (int | float | None, optional): The number of timeout [sec] for post request. If `None`, 60 (one minute) will be set. Please note that this argument is for the `jijzept` timeout and not for configuring solver settings, such as solving time.
            sync (bool, optional): Synchronous mode.
            queue_name (Optional[str], optional): Queue name.
            system_time (jm.SystemTime): Object to store system times other than upload time.
            **kwargs: SA parameters using **kwargs. If both `**kwargs` and `parameters` are exist, the value of `**kwargs` takes precedence.

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
            sampler = jz.JijSASampler(config='config.toml')

            # upload instance
            instance_id = sampler.upload_instance(problem, {'n': 5, 'd': [1,2,3,4,5]})

            # sample uploaded instance
            sample_set = sampler.sample_instance(instance_id)
            ```
        """
        check_kwargs_against_dataclass(kwargs, JijSAParameters)
        param_dict = merge_params_and_kwargs(parameters, kwargs, JijSAParameters)

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
