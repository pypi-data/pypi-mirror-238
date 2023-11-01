# -*- coding: utf-8 -*-
"""
    pip_services4_observability.count.DefaultCountersFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Default counters factory implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_services4_components.build import Factory
from pip_services4_components.refer import Descriptor

from .CompositeCounters import CompositeCounters
from .LogCounters import LogCounters
from .NullCounters import NullCounters


class DefaultCountersFactory(Factory):
    """
    Creates :class:`ICounters <pip_services4_observability.count.ICounters.ICounters>` components by their descriptors.

    See :class:`Factory <pip_services4_observability.build.Factory.Factory>`,
    :class:`NullCounters <pip_services4_observability.count.NullCounters.NullCounters>`,
    :class:`LogCounters <pip_services4_observability.count.LogCounters.LogCounters>`,
    :class:`CompositeCounters <pip_services4_observability.count.CompositeCounters.CompositeCounters>`
    """

    NullCountersDescriptor = Descriptor("pip-services", "counters", "null", "*", "1.0")
    LogCountersDescriptor = Descriptor("pip-services", "counters", "log", "*", "1.0")
    CompositeCountersDescriptor = Descriptor("pip-services", "counters", "composite", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super().__init__()
        self.register_as_type(DefaultCountersFactory.NullCountersDescriptor, NullCounters)
        self.register_as_type(DefaultCountersFactory.LogCountersDescriptor, LogCounters)
        self.register_as_type(DefaultCountersFactory.CompositeCountersDescriptor, CompositeCounters)
