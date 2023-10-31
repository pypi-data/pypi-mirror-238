# -*- coding: utf-8 -*-
"""
    pip_services4_commons.exec.IClosable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for closable components
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from abc import ABC
from typing import Optional

from pip_services4_components.context.IContext import IContext


class IClosable(ABC):
    """
    Interface for components that require explicit closure.

    For components that require opening as well as closing use :class:`IOpenable <pip_services4_commons.exec.IOpenable.IOpenable>` interface instead.

    .. code-block:: python
        class MyConnector(ICloseable):
            _client = None

            ... # The _client can be lazy created

            def close(self, context):
                if self._client is not None:
                    self._client.close()
                    self._client = null


    """

    def close(self, context: Optional[IContext]):
        """
        Closes component and frees used resources.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        raise NotImplementedError('Method from interface definition')
