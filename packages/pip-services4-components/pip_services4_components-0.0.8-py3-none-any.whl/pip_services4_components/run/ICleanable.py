# -*- coding: utf-8 -*-
"""
    pip_services4_commons.exec.ICleanable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for cleanable components
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from abc import ABC
from typing import Optional

from pip_services4_components.context.IContext import IContext


class ICleanable(ABC):
    """
    Interface for components that should clean their state.
    Cleaning state most often is used during testing.
    But there may be situations when it can be done in production.

    .. code-block:: python
        class MyObjectWithState(ICleanable):
            _state = {}
            ...

            def clear(self, context):
                self._state = {}
    """

    def clear(self, context: Optional[IContext]):
        """
        Clears component state.

        :param context: (optional) transaction id to trace execution through call chain.
        """
        raise NotImplementedError('Method from interface definition')
