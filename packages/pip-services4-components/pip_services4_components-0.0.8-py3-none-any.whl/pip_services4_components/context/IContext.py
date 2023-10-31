from abc import ABC
from typing import Any


class IContext(ABC):
    """
    Interface to specify execution context.
    """

    def get(self, key: str) -> Any:
        """
        Gets a map element specified by its key.

        :param key: a key of the element to get.
        :return: the value of the map element.
        """
        raise NotImplemented('Method not implemented')
