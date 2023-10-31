# -*- coding: utf-8 -*-
"""
    pip_services4_components.context.DefaultInfoFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Default context factory implementation

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .ContextInfo import ContextInfo
from ..build.Factory import Factory
from ..refer.Descriptor import Descriptor


class DefaultContextFactory(Factory):
    """
    Creates information components by their descriptors.

    See :class:`IFactory <pip_services4_components.build.IFactory.IFactory>`,
    :class:`ContextInfo <pip_services4_components.context.ContextInfo.ContextInfo>`
    """

    ContextInfoDescriptor = Descriptor("pip-services", "context-info", "default", "*", "1.0")
    ContainerInfoDescriptor = Descriptor("pip-services", "container-info", "default", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super().__init__()
        self.register_as_type(DefaultContextFactory.ContextInfoDescriptor, ContextInfo)
        self.register_as_type(DefaultContextFactory.ContainerInfoDescriptor, ContextInfo)
