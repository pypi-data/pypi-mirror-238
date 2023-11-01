# -*- coding: utf-8 -*-
"""
    pip_services4_observability.log.DefaultLoggerFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Default logger factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_services4_components.build import Factory
from pip_services4_components.refer import Descriptor

from .CompositeLogger import CompositeLogger
from .ConsoleLogger import ConsoleLogger
from .NullLogger import NullLogger


class DefaultLoggerFactory(Factory):
    """
    Creates :class:`ILogger <pip_services4_observability.log.ILogger.ILogger>` components by their descriptors.

    See :class:`Factory <pip_services4_observability.build.Factory.Factory>`,
    :class:`NullLogger <pip_services4_observability.log.NullLogger.NullLogger>`,
    :class:`ConsoleLogger <pip_services4_observability.log.ConsoleLogger.ConsoleLogger>`,
    :class:`CompositeLogger <pip_services4_observability.log.CompositeLogger.CompositeLogger>`
    """

    NullLoggerDescriptor = Descriptor("pip-services", "logger", "null", "*", "1.0")
    ConsoleLoggerDescriptor = Descriptor("pip-services", "logger", "console", "*", "1.0")
    CompositeLoggerDescriptor = Descriptor("pip-services", "logger", "composite", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super().__init__()
        self.register_as_type(DefaultLoggerFactory.NullLoggerDescriptor, NullLogger)
        self.register_as_type(DefaultLoggerFactory.ConsoleLoggerDescriptor, ConsoleLogger)
        self.register_as_type(DefaultLoggerFactory.CompositeLoggerDescriptor, CompositeLogger)
