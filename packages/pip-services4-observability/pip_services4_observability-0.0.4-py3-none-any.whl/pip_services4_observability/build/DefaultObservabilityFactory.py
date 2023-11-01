from pip_services4_components.build import Factory
from pip_services4_components.refer import Descriptor
from pip_services4_observability.trace import NullTracer, LogTracer, CompositeTracer

from pip_services4_observability.log import NullLogger, ConsoleLogger, CompositeLogger

from pip_services4_observability.count import NullCounters, LogCounters, CompositeCounters


class DefaultObservabilityFactory(Factory):
    """
    Creates observability components by their descriptors.
    See:
    :class:`Factory <pip_services4_components.build.Factory.Factory>`
    :class:`NullCounters <pip_services4_observability.count.NullCounters.NullCounters>`
    :class:`LogCounters <pip_services4_observability.log.LogCounters.LogCounters>`
    :class:`CompositeCounters <pip_services4_observability.count.CompositeCounters.CompositeCounters>`
    """
    NullCountersDescriptor = Descriptor("pip-services", "counters", "null", "*", "1.0")
    LogCountersDescriptor = Descriptor("pip-services", "counters", "log", "*", "1.0")
    CompositeCountersDescriptor = Descriptor("pip-services", "counters", "composite", "*", "1.0")
    NullLoggerDescriptor = Descriptor("pip-services", "logger", "null", "*", "1.0")
    ConsoleLoggerDescriptor = Descriptor("pip-services", "logger", "console", "*", "1.0")
    CompositeLoggerDescriptor = Descriptor("pip-services", "logger", "composite", "*", "1.0")
    NullTracerDescriptor = Descriptor("pip-services", "tracer", "null", "*", "1.0")
    LogTracerDescriptor = Descriptor("pip-services", "tracer", "log", "*", "1.0")
    CompositeTracerDescriptor = Descriptor("pip-services", "tracer", "composite", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super().__init__()
        self.register_as_type(DefaultObservabilityFactory.NullCountersDescriptor, NullCounters)
        self.register_as_type(DefaultObservabilityFactory.LogCountersDescriptor, LogCounters)
        self.register_as_type(DefaultObservabilityFactory.CompositeCountersDescriptor, CompositeCounters)
        self.register_as_type(DefaultObservabilityFactory.NullLoggerDescriptor, NullLogger)
        self.register_as_type(DefaultObservabilityFactory.ConsoleLoggerDescriptor, ConsoleLogger)
        self.register_as_type(DefaultObservabilityFactory.CompositeLoggerDescriptor, CompositeLogger)
        self.register_as_type(DefaultObservabilityFactory.NullTracerDescriptor, NullTracer)
        self.register_as_type(DefaultObservabilityFactory.LogTracerDescriptor, LogTracer)
        self.register_as_type(DefaultObservabilityFactory.CompositeTracerDescriptor, CompositeTracer)
