from typing import Any

from pip_services4_commons.data import AnyValueMap

from pip_services4_components.config import ConfigParams
from pip_services4_components.context import IContext
from ..exec.Parameters import Parameters


class Context(IContext):
    """
    Basic implementation of an execution context.

    See :class:`IContext <pip_services4_components.context.IContext.IContext>`
    See :class:`AnyValueMap <pip_services4_commons.data.AnyValueMap.AnyValueMap>`
    """

    def __init__(self, values: Any):
        """
        Gets a map element specified by its key.

        :param values: a key of the element to get.
        :return: the value of the map element.
        """
        self._values = AnyValueMap(values)

    def get(self, key: str) -> Any:
        return self._values.get(key)

    @staticmethod
    def from_value(value: Any) -> 'Context':
        """
        Creates a new instance of the map and assigns its value.

        :param value: (optional) values to initialize this map.
        """
        return Context(value)

    @staticmethod
    def from_tuples(*tuples: Any) -> 'Context':
        """
        Creates a new Context object filled with provided key-value pairs called tuples.
        Tuples parameters contain a sequence of key1, value1, key2, value2, ... pairs.

        :param tuples: the tuples to fill a new Parameters object.
        :return: a new Parameters object.

        """

        obj = AnyValueMap.from_tuples(*tuples)
        return Context(obj)

    @staticmethod
    def from_config(config: ConfigParams) -> 'Context':
        """
        Creates new Context from ConfigMap object.

        :param config: a ConfigParams that contain parameters.
        :return: a new Context object.

        See :class:`ConfigParams <pip_services4_components.config.ConfigParams.ConfigParams>`
        """
        if not config:
            return Context()

        values = AnyValueMap()
        for key in config:
            if config.get(key):
                values.put(key, config.get(key))

        return Context()

    @staticmethod
    def from_trace_id(trace_id: str) -> 'Context':
        """
        Creates new Context from trace id.
        :param trace_id: a transaction id to trace execution through call chain.
        :return: a new Parameters object.
        """
        return Context(Parameters.from_tuples("trace_id", trace_id))
