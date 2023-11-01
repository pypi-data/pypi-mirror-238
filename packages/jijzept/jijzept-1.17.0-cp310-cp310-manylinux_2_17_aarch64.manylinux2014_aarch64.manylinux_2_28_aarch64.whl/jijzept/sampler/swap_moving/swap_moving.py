from __future__ import annotations

import dataclasses
import typing as typ
import warnings

from numbers import Number

import jijmodeling as jm
import numpy as np

from jijmodeling import Problem

from jijzept.client import JijZeptClient
from jijzept.entity.schema import SolverType
from jijzept.response import JijModelingResponse
from jijzept.sampler.base_sampler import (
    JijZeptBaseSampler,
    ParameterSearchParameters,
    check_kwargs_against_dataclass,
    merge_params_and_kwargs,
    sample_model,
)
from jijzept.sampler.openjij import JijSAParameters

NHOT_CONSTRAINTS = typ.List[typ.Tuple[typ.List[int], int]]
"""N-hot constraint indices.

x0 + x1 + x2 = 3,
x3 + x4 + x5 = 1
-> [([0, 1, 2], 3), ([3, 4, 5], 1)]
"""


def _nhot_problem(
    qubo, constant: float, constraints: NHOT_CONSTRAINTS, is_hubo: bool = False
):
    """Creates an optimization problem that incorporates n-hot constraints based on the provided QUBO problem.

    Args:
        qubo: A dictionary representing the QUBO problem, where the keys are tuples of indices and the values are floats representing the weight of the term.
        constant: The constant term in the QUBO problem.
        constraints: A list of tuples, where each tuple contains a list of indices corresponding to the variables involved in the n-hot constraint and the number of variables that should be in the ON state.
        is_hubo: A flag to indicate whether to use HUBO instead of QUBO.

    Returns:
        - A `Problem` instance representing the QUBO problem with n-hot constraints.
        - A dictionary containing instance data needed to solve the problem.
        - A dictionary mapping variable names to indices in the QUBO problem.
    """
    if is_hubo:
        problem, instance_data, key_map, deci_var = hubo_problem(qubo, constant)
    else:
        problem, instance_data, key_map, deci_var = qubo_problem(qubo, constant)

    # nhot_indices = jm.JaggedArray("nhot_indice", dim=2)
    # nhot_num = jm.Placeholder("nhot_num")
    # nhot_const = jm.Placeholder("nhot_const", dim=1)
    # i = jm.Element("i", nhot_num)
    # k = jm.Element("k", nhot_indices[i])
    # x = deci_var["x"]
    # # problem += jm.Constraint("nhot", jm.Sum(k, x[k]) == nhot_const[i], forall=i)
    # problem += jm.Constraint("nhot", jm.Sum(k, x[k]) == nhot_const[i], forall=i)

    # nhot_indices_data = [_indices for _indices, _ in constraints]
    # nhot_const_data = [_value for _, _value in constraints]

    # instance_data["nhot_indices"] = nhot_indices_data
    # instance_data["nhot_const"] = nhot_const_data
    # instance_data["nhot_num"] = np.array(len(nhot_indices_data))

    # TODO: We have to fix this handle. Now, above model cannot run on JijZept.
    _nhot_constraint_data: dict[int, list] = {}
    if constraints is not None:
        for _nhot_indices, _n_value in constraints:
            if _n_value not in _nhot_constraint_data:
                _nhot_constraint_data[_n_value] = []
            _nhot_constraint_data[_n_value].append(_nhot_indices)

    x = deci_var["x"]
    if _nhot_constraint_data is not None:
        for _n_value, _nhot_indices in _nhot_constraint_data.items():
            const_name = f"{_n_value}hot_const"

            jagged_array_name = f"{_n_value}hot_indices"
            nhot_indices = jm.JaggedArray(jagged_array_name, dim=2)
            nhot_num = len(_nhot_indices)
            i = jm.Element("i", belong_to=nhot_num)
            k = jm.Element("k", belong_to=nhot_indices[i])
            problem += jm.Constraint(const_name, jm.sum(k, x[k]) == _n_value, forall=i)
            instance_data[jagged_array_name] = _nhot_indices

    return problem, instance_data, key_map


def sample_nhot(
    is_hubo: bool,
    client: JijZeptClient,
    solver: str,
    queue_name: str,
    qubo: dict[tuple[int, int], float],
    constant: float,
    max_wait_time: int | float | None,
    sync: bool,
    constraints: NHOT_CONSTRAINTS,
    **kwargs,
):
    """Sample from a QUBO or Ising Hamiltonian with NHOT constraints using D-Wave's quantum annealer.

    Args:
        is_hubo (bool): Whether the input problem is a HUBO or not.
        client (JijZeptClient): A JijZeptClient instance.
        solver (str): The name of the D-Wave solver to use.
        queue_name (str): The name of the D-Wave queue to use.
        qubo (dict[tuple[int, int], float]): The input QUBO or Ising Hamiltonian.
        constant (float): The constant offset for the Hamiltonian.
        max_wait_time (int | float | None): Maximum time to wait for the solver in seconds. If None, waits indefinitely.
        sync (bool): Whether to wait for the results to complete before returning.
        constraints (NHOT_CONSTRAINTS): The NHOT constraints to apply to the problem.
        **kwargs: Additional keyword arguments to pass to `sample_model`.

    Returns:
        SampleSet: The sample set obtained from the solver.
    """
    qubo_model, instance_data, var_map = _nhot_problem(
        qubo, constant, constraints, is_hubo
    )
    parameters = ParameterSearchParameters(
        multipliers={}, mul_search=False, normalize_qubo=False
    )
    sample_set = sample_model(
        client=client,
        solver=solver,
        queue_name=queue_name,
        problem=qubo_model,
        instance_data=instance_data,
        fixed_variables={},
        parameter_search_parameters=parameters,
        max_wait_time=max_wait_time,
        sync=sync,
        normalize=False,
        **kwargs,
    )
    sample_set.set_variable_labels(var_map)
    return sample_set


@dataclasses.dataclass
class JijSwapMovingParameters:
    """Manage Parameters for using JijSwapMovingSampler.

    Attributes:
        constraints (Optional[list], optional): Constraint term. x0+x1=1 and x2+x3=1 is written as [([0,1], 1), ([2,3], 1)].
        penalties (Optional[list], optional): Penalty term. 1.3(0.1x1+0.2x2+0.3x3-1)^2 is written as [(1.3, {1:0.1, 2:0.2, 3:0.3}, 1)].
        beta_min (Optional[float], optional): Minimum (initial) inverse temperature. If `None`, this will be set automatically.
        beta_max (Optional[float], optional): Maximum (final) inverse temperature. If `None`, this will be set automatically.
        num_sweeps (Optional[int], optional): The number of Monte-Carlo steps. If `None`, 1000 will be set.
        num_reads (Optional[int], optional): The number of samples. If `None`, 1 will be set.
        initial_state (Optional[dict], optional): Initial state. If `None`, this will be set automatically.
        updater (Optional[str], optional): Updater algorithm. "single spin flip" or "swendsen wang". If `None`, "single spin flip" will be set.
        sparse (Optional[bool], optional): If `True`, only non-zero matrix elements are stored, which will save memory. If `None`, `False` will be set.
        reinitialize_state (Optional[bool], optional): If `True`, reinitialize state for each run. If `None`, `True` will be set.
        seed (Optional[int], optional): Seed for Monte Carlo algorithm. If `None`, this will be set automatically.
    """

    constraints: list | None = None
    penalties: list | None = None
    beta_min: float | None = None
    beta_max: float | None = None
    num_sweeps: int | None = None
    num_reads: int | None = None
    initial_state: list | dict | None = None
    updater: str | None = None
    sparse: bool | None = None
    reinitialize_state: bool | None = None
    seed: int | None = None


class JijSwapMovingSampler(JijZeptBaseSampler):
    """A sampler class for JijSwapMoving."""

    solver_type: SolverType = SolverType(queue_name="swapmovingsolver", solver="SA")
    jijmodeling_solver_type = SolverType(
        queue_name="swapmovingsolver", solver="SAParaSearch"
    )

    def __init__(
        self,
        token: str = None,
        url: str | dict = None,
        proxy=None,
        config=None,
        config_env="default",
    ):
        """Sets token and url.

        Args:
            token (str, optional): Token string. Defaults to None.
            url (Union[str, dict], optional): API URL. Defaults to None.
            proxy (str, optional): Proxy URL. Defaults to None.
            config (str, optional): Config file path. Defaults to None.

        Raises:
            :obj:`TypeError`: `token`, `url`, or `config` is not str.
        """
        warnings.warn(
            message="JijSwapMovingSampler is deprecated. Please use other samplers.",
            stacklevel=2,
        )
        self.client = JijZeptClient(
            url=url, token=token, proxy=proxy, config=config, config_env=config_env
        )

    @property
    def properties(self):
        """Returns a dictionary of properties for the model."""
        return dict()

    @property
    def parameters(self):
        """Returns a dictionary of parameters for the model."""
        return dict()

    def _select_index_type_from_interactions(self, J: dict | None = None):
        """Determines the index type from the given interaction terms dictionary.

        Args:
            J (dict|None): A dictionary of interaction terms (default=None).

        Returns:
            str: A string indicating the index type for the interaction terms.

        Raises:
            TypeError: If the interaction terms are invalid.
        """
        if J is None:
            return "IndexType.INT"
        elif isinstance(J, dict):
            if len(J) == 0:
                return "IndexType.INT"
            else:
                for key in J.keys():
                    if not isinstance(key, tuple):
                        raise TypeError("Invalid Interactions")
                    else:
                        for i in range(len(key)):
                            if isinstance(key[i], int):
                                return "IndexType.INT"
                            elif isinstance(key[i], str):
                                return "IndexType.STRING"
                            elif isinstance(key[i], tuple):
                                if len(key[i]) == 2:
                                    return "IndexType.INT_TUPLE_2"
                                elif len(key[i]) == 3:
                                    return "IndexType.INT_TUPLE_3"
                                elif len(key[i]) == 4:
                                    return "IndexType.INT_TUPLE_4"
                        raise TypeError("Invalid Interactions")
        else:
            raise TypeError("Invalid Interactions")

    def _select_index_type_from_linear(self, h: dict | None = None):
        """Determine the index type from the given linear terms dictionary.

        Args:
            h (dict | None): A dictionary of linear terms. Each key represents a variable or a tuple of variables.

        Returns:
            str: A string indicating the index type of the linear terms. Possible values
                are "IndexType.INT", "IndexType.STRING", "IndexType.INT_TUPLE_2", "IndexType.INT_TUPLE_3", or
                "IndexType.INT_TUPLE_4".

        Raises:
            TypeError: If the linear terms dictionary is invalid, meaning that it's not a dictionary or contains keys that
                    are not integers, strings, or tuples of integers or strings.
        """
        if h is None:
            return "IndexType.INT"
        elif isinstance(h, dict):
            if len(h) == 0:
                return "IndexType.INT"
            else:
                for key in h.keys():
                    if isinstance(key, int):
                        return "IndexType.INT"
                    elif isinstance(key, str):
                        return "IndexType.STRING"
                    elif isinstance(key, tuple) and len(key) == 2:
                        return "IndexType.INT_TUPLE_2"
                    elif isinstance(key, tuple) and len(key) == 3:
                        return "IndexType.INT_TUPLE_3"
                    elif isinstance(key, tuple) and len(key) == 4:
                        return "IndexType.INT_TUPLE_4"
                    raise TypeError("Invalid linear terms")
        else:
            raise TypeError("Invalid linear terms")

    def sample_model(
        self,
        problem: Problem,
        feed_dict: dict[str, Number | list | np.ndarray],
        multipliers: dict[str, Number] = {},
        fixed_variables: dict[str, dict[tuple[int, ...], int | float]] = {},
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

        To configure the solver, instantiate the `JijSwapMovingParameters` class and pass the instance to the `parameters` argument.

        Args:
            problem (Problem): Mathematical expression of JijModeling. The decision variable type should be Binary.
            feed_dict (Dict[str, Union[Number, list, np.ndarray]]): The actual values to be assigned to the placeholders.
            multipliers (Dict[str, Number], optional): The actual multipliers for penalty terms, derived from constraint conditions.
            fixed_variables (Dict[str, Dict[Tuple[int, ...], Union[int, float]]]): dictionary of variables to fix.
            needs_square_dict (Dict[str, bool], optional): If `True`, the corresponding constraint is squared when added as a penalty to the QUBO. When the constraint label is not added to the 'needs_square_dict', it defaults to `True` for linear constraints and `False` for non-linear constraints.
            search (bool, optional): If `True`, the parameter search will be carried out, which tries to find better values of multipliers for penalty terms.
            num_search (int, optional): The number of parameter search iteration. Defaults to set 15. This option works if `search` is `True`.
            algorithm (Optional[str], optional): Algorithm for parameter search. Defaults to None.
            parameters (JijSwapMovingParameters | None): defaults None.
            max_wait_time (int | float | None, optional): The number of timeout [sec] for post request. If `None`, 60 (one minute) will be set. Please note that this argument is for the `jijzept` timeout and not for configuring solver settings, such as solving time.
            sync (bool, optional): Synchronous mode.
            queue_name (Optional[str], optional): Queue name.
            **kwargs: SwapMoving parameters using **kwargs. If both `**kwargs` and `parameters` are exist, the value of `**kwargs` takes precedence.

        Returns:
            JijModelingResponse: Stores minimum energy samples and other information.

        Examples:
            ```python
            import jijzept as jz
            import jijmodeling as jm
            n = jm.Placeholder('n')
            x = jm.Binary('x', shape=n)
            d = jm.Placeholder('d', shape=n)
            i = jm.Element("i", n)
            problem = jm.Problem('problem')
            problem += jm.Sum(i, d[i] * x[i])
            problem += jm.Constraint("one-hot", jm.Sum(i, x[i]) == 1)
            sampler = jz.JijSwapMovingSampler(config='config.toml')
            response = sampler.sample_model(problem, feed_dict={'n': 5, 'd': [1,2,3,4,5]})
            ```
        """
        check_kwargs_against_dataclass(kwargs, JijSwapMovingParameters)
        param_dict = merge_params_and_kwargs(
            parameters, kwargs, JijSwapMovingParameters
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
