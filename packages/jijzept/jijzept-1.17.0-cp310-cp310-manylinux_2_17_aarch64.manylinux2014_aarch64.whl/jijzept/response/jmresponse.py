from __future__ import annotations

from typing import Any, Optional
import warnings

import jijmodeling as jm

from jijzept.response.base import BaseResponse


class JijModelingResponse(BaseResponse):
    """Return object from JijZept."""

    def __init__(self, sample_set: Optional[jm.SampleSet] = None):
        if sample_set is None:
            self._sample_set = jm.SampleSet(
                record=jm.Record({"x": []}, [0]),
                evaluation=jm.Evaluation([]),
                measuring_time=jm.MeasuringTime(),
            )
        else:
            self._sample_set = sample_set
        super().__init__()

    @classmethod
    def from_json_obj(cls, json_obj) -> Any:
        """Generate object from JSON object.

        Args:
            json_obj (str): JSON object

        Returns:
            Any: object
        """
        return cls(jm.SampleSet.from_json(json_obj["sample_set"]))

    @classmethod
    def empty_data(cls) -> Any:
        """Create an empty object.

        Returns:
            Any: Empty object.
        """
        return cls()

    def __repr__(self):
        """Return the representation of the object."""
        return self.sample_set.__repr__()

    def __str__(self):
        """Return the string representation of the object."""
        return BaseResponse.__repr__(self) + "\n" + self.sample_set.__str__()

    def set_variable_labels(self, var_labels: dict[int, str]):
        """Set variable labels.

        Args:
            var_labels (dict[int, str]): Dictionary of variable labels.
        """
        self._variable_labels = var_labels

    @property
    def variable_labels(self) -> dict[int, str]:
        """Return variable labels.

        Returns:
            dict[int, str]: Dictionary of variable labels.
        """
        return self._variable_labels

    @property
    def sample_set(self) -> jm.SampleSet:
        warnings.warn(
            (
                "This column oriented sample set will be deprecated in the future. "
                "Please migrate to the row oriented sample set using `get_sampleset`."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return self._sample_set

    @property
    def record(self) -> jm.Record:
        return self.sample_set.record

    @property
    def evaluation(self) -> jm.Evaluation:
        return self.sample_set.evaluation

    @property
    def measuring_time(self) -> jm.MeasuringTime:
        return self.sample_set.measuring_time

    @property
    def metadata(self) -> dict:
        return self.sample_set.metadata

    def feasible(
        self,
        rtol: float = 0.00001,
        atol: float = 1e-8,
    ) -> jm.SampleSet:
        """
        Return a Sampleset with only feasible solutions. If there is no feasible solution, the record and evaluation are empty.

        Args:
            rtol (float): The relative tolerance parameter. Defaults to 1e-5.
            atol (float): The absolute tolerance parameter. Defaults to 1e-8.

        Returns:
            SampleSet: A SampleSet object with only feasible solutions or empty.

        Note:
            The feasible solutions are determined by the following condition: $$ |0 - v| \\\\leq \\\\mathrm{atol} + \\\\mathrm{rtol} \\\\cdot |v| $$
        """
        return self.sample_set.feasible(rtol, atol)

    def infeasible(
        self,
        rtol: float = 0.00001,
        atol: float = 1e-8,
    ) -> jm.SampleSet:
        """
        Return a Sampleset with only infeasible solutions. If there is no infeasible solution, the record and evaluation are empty.

        Args:
            rtol (float): The relative tolerance parameter. Defaults to 1e-5.
            atol (float): The absolute tolerance parameter. Defaults to 1e-8.

        Returns:
            SampleSet: A SampleSet object with only infeasible solutions or empty.

        Note:
            The feasible solutions are determined by the following condition: $$ |0 - v| > \\\\mathrm{atol} + \\\\mathrm{rtol} \\\\cdot |v| $$
        """
        return self.sample_set.infeasible(rtol, atol)

    def is_dense(self) -> jm.SampleSet:
        """
        Return true if the solution is dense.

        Returns:
            bool: True if the solution is dense.
        """
        return self.sample_set.is_dense()

    def is_sparse(self) -> jm.SampleSet:
        """
        Return true if the solution is sparse.

        Returns:
            bool: True if the solution is sparse.
        """
        return self.sample_set.is_sparse()

    def lowest(self, rtol: float = 0.00001, atol: float = 1e-8) -> jm.SampleSet:
        """
        Return a Sampleset with feasible solutions which has the lowest objective. If there is no feasible solution, the record and evaluation are empty.

        Args:
            rtol (float): The relative tolerance parameter. Defaults to 1e-5.
            atol (float): The absolute tolerance parameter. Defaults to 1e-8.

        Returns:
            SampleSet: A SampleSet object with feasible solutions or empty.

        Note:
            The feasible solutions are determined by the following condition: $$ |0 - v| ¥leq ¥mathrm{atol} + ¥mathrm{rtol} ¥cdot |v| $$
        """
        return self.sample_set.lowest(rtol, atol)

    def to_dense(self) -> jm.SampleSet:
        """
        Return a Sampleset whose record is converted into a dense solution format. If the record is already a dense solution format, return itself.

        Returns:
            SampleSet: A SampleSet object.
        """
        return self.sample_set.to_dense()

    def to_pandas(self):
        """
        Convert into a pandas DataFrame.

        Returns:
            pandas.DataFrame: A pandas DataFrame.
        """
        return self.sample_set.to_pandas()

    def to_json(self) -> str:
        """
        Serialize the SampleSet object into a JSON string.

        Returns:
            str: A JSON string.

        Note:
            A numpy array is converted into a list.
        """
        return self.sample_set.to_json()
    
    def get_sampleset(self) -> jm.experimental.SampleSet:
        """
        Return a row oriented SampleSet object.

        Returns:
            jm.experimental.SampleSet: A row oriented SampleSet object.
        """
        return jm.experimental.from_old_sampleset(self._sample_set)
