# -*- coding: utf-8 -*-
from typing import Optional, List

from pip_services4_components.refer import IReferences, IReferenceable, Descriptor
from pip_services4_components.context.IContext import IContext

from pip_services4_observability.trace.ITracer import ITracer
from pip_services4_observability.trace.TraceTiming import TraceTiming


class CompositeTracer(ITracer, IReferenceable):
    """
    Aggregates all tracers from component references under a single component.

    It allows to record traces and conveniently send them to multiple destinations.

    ### References ###
        - `\*:tracer:\*:\*:1.0`     (optional) :class:`ITracer <pip_services4_observability.trace.ITracer.ITracer>` components to pass operation traces

    See :class:`ITracer <pip_services4_observability.trace.ITracer.ITracer>`

     Example:

    .. code-block:: python
        class MyComponent(IReferenceable):
            def __init__(self):
                self.__tracer = CompositeTracer()

            def set_references(self, references: IReferences):
                self.__tracer.set_references(references)
                ...

            def my_method(self, context):
                timing = self.__tracer.begin_trace(context, "mycomponent", "mymethod")
                try:
                    ...
                    timing.end_trace()
                except Exception as err:
                    timing.end_failure(err)

    """
    _TRACERS: List[ITracer] = []

    def __init__(self, references: IReferences = None):
        """
        Creates a new instance of the tracer.

        :param references: references to locate the component dependencies.
        """
        if references is not None:
            self.set_references(references)

    def set_references(self, references: IReferences):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        traces = references.get_optional(Descriptor(None, "tracer", None, None, None))
        for i in range(len(traces)):
            tracer = traces[i]

            if tracer != self:
                self._TRACERS.append(tracer)

    def trace(self, context: Optional[IContext], component: str, operation: str, duration: float) -> None:
        """
        Records an operation trace with its name and duration

        :param context: (optional) transaction id to trace execution through call chain.
        :param component: a name of called component
        :param operation: a name of the executed operation.
        :param duration: execution duration in milliseconds.
        """
        for tracer in self._TRACERS:
            tracer.trace(context, component, operation, duration)

    def failure(self, context: Optional[IContext], component: str, operation: str, error: Exception, duration: float):
        """
        Records an operation failure with its name, duration and error

        :param context: (optional) transaction id to trace execution through call chain.
        :param component: a name of called component
        :param operation: a name of the executed operation.
        :param error: an error object associated with this trace.
        :param duration: execution duration in milliseconds.
        """
        for tracer in self._TRACERS:
            tracer.failure(context, component, operation, error, duration)

    def begin_trace(self, context: Optional[IContext], component: str, operation: str) -> TraceTiming:
        """
        Begings recording an operation trace

        :param context: (optional) transaction id to trace execution through call chain.
        :param component: a name of called component
        :param operation: a name of the executed operation.
        :return: a trace timing object.
        """
        return TraceTiming(context, component, operation, self)
