# -*- coding: utf-8 -*-
from pip_services4_components.build import Factory
from pip_services4_components.refer import Descriptor

from pip_services4_observability.trace.CompositeTracer import CompositeTracer
from pip_services4_observability.trace.LogTracer import LogTracer
from pip_services4_observability.trace.NullTracer import NullTracer


class DefaultTracerFactory(Factory):
    """
    Creates :class:`ITracer <pip_services4_observability.trace.ITracer.ITracer>` components by their descriptors.

    See :class:`Factory <pip_services4_observability.build.Factory.Factory>`,
    :class:`NullTracer <pip_services4_observability.trace.NullTracer.NullTracer>`,
    :class:`ConsoleTracer <pip_services4_observability.trace.ConsoleTracer.ConsoleTracer>`,
    :class:`CompositeTracer <pip_services4_observability.trace.CompositeTracer.CompositeTracer>`

    """

    NullTracerDescriptor = Descriptor("pip-services", "tracer", "null", "*", "1.0")
    LogTracerDescriptor = Descriptor("pip-services", "tracer", "log", "*", "1.0")
    CompositeTracerDescriptor = Descriptor("pip-services", "tracer", "composite", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super(DefaultTracerFactory, self).__init__()
        self.register_as_type(DefaultTracerFactory.NullTracerDescriptor, NullTracer)
        self.register_as_type(DefaultTracerFactory.LogTracerDescriptor, LogTracer)
        self.register_as_type(DefaultTracerFactory.CompositeTracerDescriptor, CompositeTracer)
