# -*- coding: utf-8 -*-
"""
    pip_services_common.refer.ReferenceException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Reference error type
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from typing import Any, Optional

from pip_services4_commons.errors import InternalException

from ..context.ContextResolver import ContextResolver
from ..context.IContext import IContext


class ReferenceException(InternalException):
    """
    Error when __required component dependency cannot be found.
    """

    def __init__(self, context: Optional[IContext] = None, locator: Any = None):
        """
        Creates an error instance and assigns its values.

        :param context: (optional) a unique transaction id to trace execution through call chain.

        :param locator: the locator to find reference to dependent component.
        """
        message = 'Cannot locate reference: ' + (str(locator) if not (locator is None) else '<None>')
        super(ReferenceException, self).__init__(ContextResolver.get_trace_id(context), "REF_ERROR", message)
        self.with_details('locator', locator)
