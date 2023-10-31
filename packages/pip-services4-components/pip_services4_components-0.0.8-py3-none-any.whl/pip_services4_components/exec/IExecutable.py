# -*- coding: utf-8 -*-
"""
    pip_services4_commons.exec.IExecutable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for executable components with parameters
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from abc import ABC
from typing import Optional

from pip_services4_components.context.IContext import IContext

from ..exec.Parameters import Parameters


class IExecutable(ABC):
    """
    Interface for components that can be called to execute work.

    .. code-block:: python
        class EchoComponent(IExecutable):
            ...
            def execute(self, context: Optional[IContext], args: Parameters):
                result = args.get_as_object("message")
                return result

        echo = new EchoComponent()
        message = "Test";
        result = echo.execute("123", Parameters.from_tuples("message", message))
        print("Request: " + message + " Response: " + result)

    """

    def execute(self, context: Optional[IContext], args: Parameters):
        """
        Executes component with arguments and receives execution result.

        :param context: (optional) transaction id to trace execution through call chain.

        :param args: execution arguments.

        :return: execution result
        """
        raise NotImplementedError('Method from interface definition')
