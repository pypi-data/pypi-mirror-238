# -*- coding: utf-8 -*-
"""
    pip_services4_commons.exec.INotifiable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for notifiable components with parameters
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from abc import ABC
from typing import Optional

from pip_services4_components.context.IContext import IContext

from ..exec.Parameters import Parameters


class INotifiable(ABC):
    """
    Interface for components that can be asynchronously notified.
    The notification may include optional argument that describe the occured event_name

    .. code-block:: python
        class MyComponent(INotifable):
            ...
            def notify(context, args):
                print("Occured event " + args.get_as_string("event"))

        my_component = MyComponent()
        my_component.notify(Context.from_trace_id("123"), Parameters.from_tuples("event", "Test Event"));
    """

    def notify(self, context: Optional[IContext], args: Parameters):
        """
        Notifies the component about occured event_name.

        :param context: (optional) transaction id to trace execution through call chain.

        :param args: notification arguments.
        """
        raise NotImplementedError('Method from interface definition')
