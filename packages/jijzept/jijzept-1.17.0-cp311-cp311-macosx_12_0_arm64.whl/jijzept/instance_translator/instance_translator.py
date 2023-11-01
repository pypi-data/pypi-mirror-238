from __future__ import annotations

import pprint, typing

import numpy as np

from jijzept.type_annotation import InstanceData, InstanceDataValue


class InstanceTranslator:
    """A utility class for translating instance data that may contain numpy arrays to JSON-serializable formats."""

    @staticmethod
    def instance_translate(
        instance_data: InstanceData,
    ) -> dict[str, typing.Union[int, float, list]]:
        """Translates instance data that may contain numpy arrays to JSON-serializable formats.

        Args:
            instance_data (dict[str, Union[int, float, np.integer, np.floating, np.ndarray, list]]): The instance data to be translated.

        Returns:
            dict[str, Union[int, float, list]]: The translated instance data.

        Raises:
            TypeError: If the value of the dict is not a numeric type.
        """

        try:
            translated_instance_data = {
                key: InstanceTranslator.__instance_translate(instance_data_value=value)
                for key, value in instance_data.items()
            }
        except TypeError as exc:
            raise TypeError(
                f"Only numeric type values are allowed for the value of this dict."
                f"{pprint.pformat(instance_data)}"
            ) from exc
        else:
            return translated_instance_data

    @staticmethod
    def __instance_translate(
        *,
        instance_data_value: InstanceDataValue,
    ) -> typing.Union[int, float, list]:
        """Helper function to recursively translate instance data.

        Args:
            instance_data_value (Union[int, float, np.integer, np.floating, np.ndarray, list]): The instance data to be translated.

        Returns:
            Union[int, float, list]: The translated instance data.
        """

        if isinstance(instance_data_value, np.ndarray):
            return instance_data_value.tolist()
        elif isinstance(instance_data_value, list):
            return [
                InstanceTranslator.__instance_translate(instance_data_value=value)
                for value in instance_data_value
            ]
        else:
            return InstanceTranslator.__numpy_translate(value=instance_data_value)

    @staticmethod
    def __numpy_translate(
        *, value: typing.Union[int, float, np.integer, np.floating]
    ) -> typing.Union[int, float]:
        """Helper function to translate numpy values to Python numeric types.

        Args:
            value (Union[int, float, np.integer, np.floating]): The numpy value to be translated.

        Returns:
            Union[int, float]: The translated Python numeric value.

        Raises:
            TypeError: If the value is not a numeric type.
        """
        if isinstance(value, (int, float)):
            return value
        elif isinstance(value, np.integer):
            return int(value)
        elif isinstance(value, np.floating):
            return float(value)
        else:
            raise TypeError(
                f"{pprint.pformat(value)} is {type(value)} type, not number."
            )
