import enum

from abc import ABCMeta, abstractmethod
from typing import Callable, Optional, TypeVar

from jijzept.client import JijZeptClient

_FuncT = TypeVar("_FuncT", bound=Callable)
_TBaseResponse = TypeVar("_TBaseResponse", bound="BaseResponse")


class AutoName(enum.Enum):
    """Enumerate class for auto-generating the next enumerated value."""

    def _generate_next_value_(name, start, count, last_values):
        return name


class APIStatus(AutoName):
    """API Status.

    `PENDING` shows that the request has been sent but not caught by solvers.

    `RUNNING` shows that the request has been sent and caught by solvers.

    `SUCCESS` shows that solver returns the solution successfully.

    `FAILED` shows that solver fails to return solutions with some errors.

    `UNKNOWNERROR` and `VALIDATIONERROR` shows that solver fails to return solutions with some errors that is not expected.
    Please contact to Jij development team if you find this error.
    """

    SUCCESS: str = enum.auto()
    PENDING: str = enum.auto()
    RUNNING: str = enum.auto()
    FAILED: str = enum.auto()
    UNKNOWNERROR: str = enum.auto()
    VALIDATIONERROR: str = enum.auto()


class BaseResponse(metaclass=ABCMeta):
    """Abstract base class representing the response from the API."""

    @classmethod
    @abstractmethod
    def from_json_obj(cls, json_obj) -> None:
        """Abstract method for initializing object from JSON data.

        Args:
            json_obj: JSON data
        """

    @classmethod
    @abstractmethod
    def empty_data(cls) -> None:
        """Abstract method for generating empty data."""

    def _set_config(self, client: JijZeptClient, solution_id: str):
        """Set the client and solution ID for the response."""
        self._client = client
        self.solution_id = solution_id

    def set_status(self, status: APIStatus):
        """Set the status of the response."""
        self._status = status

    def set_err_dict(self, err_dict: dict):
        """Set the error dictionary of the response."""
        self._err_dict = err_dict

    @property
    def status(self):
        """Get the status of the response."""
        if hasattr(self, "_status"):
            return self._status
        else:
            return APIStatus.PENDING

    @property
    def error_message(self):
        """Get the error message of the response."""
        if hasattr(self, "_err_dict"):
            return self._err_dict
        else:
            return {}

    @classmethod
    def empty_response(
        cls, status: APIStatus, client: JijZeptClient, solution_id: str, err_dict={}
    ):
        """Generate empty_response.

        Args:
            status (APIStatus): status
            client (JijZeptClient): client
            solution_id (str): solution_id
            err_dict: error dictionary
        """
        response: cls = cls.empty_data()
        response._set_config(client, solution_id)
        response.set_status(status)
        response.set_err_dict(err_dict)
        return response

    def get_result(
        self: _TBaseResponse, solution_id: Optional[str] = None
    ) -> _TBaseResponse:
        """Get result from cloud.

        If `solution_id` is specified. use this id.
        Otherwise, use `self.solution_id`

        If status is updated. update self data

        Args:
            solution_id (Optional[str]): specified solution id. Defaults to None.

        Returns:
            _TBaseResponse: _description_
        """
        if solution_id is None:
            solution_id = self.solution_id

        if self.status in {APIStatus.PENDING, APIStatus.RUNNING}:
            response = self._client.fetch_result(solution_id)
            status = response["status"]
            if status == APIStatus.PENDING.value:
                self.set_status(APIStatus.PENDING)
                return self

            elif status == APIStatus.RUNNING.value:
                self.set_status(APIStatus.RUNNING)
                return self

            elif status == APIStatus.SUCCESS.value:
                temp_obj = self.from_json_obj(response["solution"])
                temp_obj.set_status(APIStatus.SUCCESS)
                # update myself
                self.__dict__.update(temp_obj.__dict__)
                return self

            elif status == APIStatus.FAILED.value:
                self.set_status(APIStatus.FAILED)
                # store error info
                self.set_err_dict(response["solution"])
                return self

            elif status == APIStatus.VALIDATIONERROR.value:
                self.set_status(APIStatus.VALIDATIONERROR)
                # store error info
                self.set_err_dict(response["solution"])
                return self

            elif status == APIStatus.UNKNOWNERROR.value:
                self.set_status(APIStatus.UNKNOWNERROR)
                # store error info
                self.set_err_dict(response["solution"])
                return self

            else:
                raise RuntimeError(f"Unpredicted status {status}.")
        else:
            return self

    def __repr__(self):
        """Return the string representation of the object."""
        return_str = self.status.__repr__()
        if self.status == APIStatus.FAILED:
            return_str += "\n"
            return_str += str(self.error_message)

        return return_str

    def __str__(self):
        """Return the string representation of the object."""
        return_str = self.status.__repr__()
        if self.status == APIStatus.FAILED:
            return_str += "\n"
            return_str += str(self.error_message)

        return return_str
