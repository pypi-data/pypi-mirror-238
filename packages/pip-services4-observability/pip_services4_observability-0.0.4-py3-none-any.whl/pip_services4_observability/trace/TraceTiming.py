# -*- coding: utf-8 -*-

import datetime
from typing import Optional

from pip_services4_observability.trace import ITracer
from pip_services4_components.context.IContext import IContext

class TraceTiming:
    """
    CounterTiming object returned by :func:`beginTrace <pip_services4_observability.trace.ITracer.ITracer.beginTrace>`
    to end timing of execution block and record the associated trace.

    Example:

    .. code-block:: python
        timing = tracer.begin_trace(Context.from_trace_id("mymethod.exec_time"));
        try:
            ...
            timing.endTrace();
        except Exceptions as err:
            timing.end_failure(err);

    """

    def __init__(self, context: Optional[IContext], component: str, operation: str, tracer: 'ITracer.ITracer' = None):
        self.__context = context
        self.__component = component
        self.__operation = operation
        self.__tracer = tracer
        self.__start = datetime.datetime.now().timestamp() * 1000

    def end_trace(self):
        """
        Ends timing of an execution block, calculates elapsed time
        and records the associated trace.
        """
        if self.__tracer is not None:
            elapsed = (datetime.datetime.now().timestamp() * 1000) - self.__start
            self.__tracer.trace(self.__context, self.__component, self.__operation, round(elapsed))

    def end_failure(self, error: Exception):
        """
        Ends timing of a failed block, calculates elapsed time
        and records the associated trace.

        :param error: an error object associated with this trace.
        """
        if self.__tracer is not None:
            elapsed = (datetime.datetime.now().timestamp() * 1000) - self.__start
            self.__tracer.failure(self.__context, self.__component, self.__operation, error, round(elapsed))
